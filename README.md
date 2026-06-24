# JobIQ — Microservices Backend Architecture

> End-to-end technical documentation covering service design, API contracts, data flow, inter-service communication, and infrastructure.

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Architecture Diagram](#2-architecture-diagram)
3. [Service Breakdown](#3-service-breakdown)
   - [API Gateway](#31-api-gateway--port-8000)
   - [User Service](#32-user-service--port-8001)
   - [Resume Service](#33-resume-service--port-8002)
   - [Job Service](#34-job-service--port-8003)
   - [Match Service](#35-match-service--port-8004)
   - [Salary Service](#36-salary-service--port-8005)
   - [Interview Service](#37-interview-service--port-8006)
   - [Recommendation Service](#38-recommendation-service)
4. [Infrastructure Layer](#4-infrastructure-layer)
5. [API Contract Reference](#5-api-contract-reference)
6. [Inter-Service Communication](#6-inter-service-communication)
7. [Authentication & Security](#7-authentication--security)
8. [Database Design](#8-database-design)
9. [Kafka Event Streaming](#9-kafka-event-streaming)
10. [Redis Caching Strategy](#10-redis-caching-strategy)
11. [Full Request Lifecycle](#11-full-request-lifecycle)
12. [Project Structure](#12-project-structure)
13. [Environment Variables](#13-environment-variables)
14. [Running Locally](#14-running-locally)
15. [Docker Setup](#15-docker-setup)

---

## 1. System Overview

JobIQ is a **microservices-based AI job intelligence platform** where each domain concern is isolated into its own independently deployable service. Services communicate via:

- **HTTP REST** (synchronous, via API Gateway)
- **Kafka** (asynchronous event streaming)
- **Redis** (shared cache)

| Layer | Technology |
|---|---|
| API Framework | FastAPI (Python) |
| Frontend | React.js (Vite, Port 5173) |
| Database | PostgreSQL (SQLAlchemy ORM) |
| Cache | Redis |
| Message Queue | Kafka + Zookeeper |
| Auth | JWT (Bearer Tokens) |
| Containerization | Docker + Docker Compose |

---

## 2. Architecture Diagram

```
                         ┌─────────────────────────────────────┐
                         │           React Frontend             │
                         │         http://localhost:5173        │
                         └──────────────┬──────────────────────┘
                                        │ HTTP (Axios + JWT)
                                        ▼
                         ┌─────────────────────────────────────┐
                         │           API Gateway                │
                         │         http://localhost:8000        │
                         │   - Auth middleware (JWT verify)     │
                         │   - Route proxying                   │
                         │   - CORS handling                    │
                         └────┬──────┬──────┬──────┬──────┬────┘
                              │      │      │      │      │
              ┌───────────────┘      │      │      │      └──────────────────┐
              ▼                      ▼      ▼      ▼                         ▼
    ┌──────────────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐
    │  User Service    │  │  Resume  │  │   Job    │  │  Salary  │  │  Interview   │
    │  :8001           │  │ Service  │  │ Service  │  │ Service  │  │  Service     │
    │  - Register      │  │  :8002   │  │  :8003   │  │  :8005   │  │  :8006       │
    │  - Login         │  │ - Parse  │  │ - CRUD   │  │ - Predict│  │  - Generate  │
    │  - JWT issue     │  │ - NLP    │  │ - Search │  │ - ML     │  │  - Questions │
    └──────┬───────────┘  └──────┬───┘  └──────┬───┘  └──────────┘  └──────────────┘
           │                     │              │
           └──────────┬──────────┘              │
                      ▼                         ▼
         ┌──────────────────────┐   ┌───────────────────────┐
         │   Match Service      │   │  Recommendation Svc   │
         │   :8004              │   │  (internal)           │
         │   - Skill matching   │   │  - Personalized feed  │
         │   - Score ranking    │   └───────────────────────┘
         └──────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │PostgreSQL│  │  Redis   │  │  Kafka   │
  │  :5432   │  │  :6379   │  │  :9092   │
  └──────────┘  └──────────┘  └──────────┘
```

---

## 3. Service Breakdown

### 3.1 API Gateway — Port 8000

**Responsibility:** Single entry point for all client requests. Handles JWT verification, request routing, CORS, and rate limiting.

**Key Files:**
```
backend/api-gateway/
├── app/
│   ├── main.py          # FastAPI app, CORS setup, route inclusion
│   ├── middleware.py    # JWT auth middleware
│   ├── routers/
│   │   ├── auth.py      # Proxy to user-service
│   │   ├── resume.py    # Proxy to resume-service
│   │   ├── jobs.py      # Proxy to job-service
│   │   └── reports.py   # Aggregator (calls multiple services)
│   └── utils/
│       └── http_client.py  # httpx async client for service calls
└── requirements.txt
```

**Endpoints exposed:**
```
POST   /users/login           → proxied to user-service:8001
POST   /users/                → proxied to user-service:8001
GET    /users/{user_id}       → proxied to user-service:8001
POST   /upload-resume/        → proxied to resume-service:8002
GET    /jobs/                 → proxied to job-service:8003
POST   /full-report           → aggregates salary + interview + match
GET    /health                → gateway health check
```

**CORS Config:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### 3.2 User Service — Port 8001

**Responsibility:** User registration, login, profile management, JWT token issuance.

**Key Files:**
```
backend/user-service/
├── app/
│   ├── main.py
│   ├── models.py        # SQLAlchemy User model
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── auth.py          # JWT creation + verification (python-jose)
│   ├── crud.py          # DB operations
│   └── database.py      # PostgreSQL connection (SQLAlchemy)
└── requirements.txt
```

**Database Table: `users`**
```sql
CREATE TABLE users (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR NOT NULL,
    email       VARCHAR UNIQUE NOT NULL,
    password    VARCHAR NOT NULL,   -- bcrypt hashed
    created_at  TIMESTAMP DEFAULT NOW()
);
```

**Endpoints:**
```
POST /users/           → Register new user
POST /users/login      → Returns JWT access_token
GET  /users/{user_id}  → Get user profile
```

**JWT Payload:**
```json
{
  "sub": "user_id",
  "exp": 1700000000
}
```

---

### 3.3 Resume Service — Port 8002

**Responsibility:** Accept PDF/DOCX resume uploads, parse content, extract skills, experience, and education using NLP.

**Key Files:**
```
backend/resume-service/
├── app/
│   ├── main.py
│   ├── parser.py        # PyMuPDF / pdfplumber extraction
│   ├── nlp.py           # spaCy / regex skill extractor
│   ├── models.py        # Resume DB model
│   ├── schemas.py
│   └── database.py
└── requirements.txt
```

**Database Table: `resumes`**
```sql
CREATE TABLE resumes (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER REFERENCES users(id),
    raw_text    TEXT,
    skills      TEXT[],             -- extracted skill list
    experience  JSONB,              -- parsed experience blocks
    education   JSONB,
    uploaded_at TIMESTAMP DEFAULT NOW()
);
```

**Endpoints:**
```
POST /upload-resume/        → Multipart file upload, returns parsed resume JSON
GET  /resume/{user_id}      → Fetch latest parsed resume for user
```

**Parsed Resume Response:**
```json
{
  "user_id": 1,
  "skills": ["Python", "FastAPI", "React", "Docker"],
  "experience": [
    { "role": "Full Stack Developer", "company": "XYZ", "years": 1 }
  ],
  "education": [
    { "degree": "B.Tech IT", "institute": "IEC College", "year": 2027 }
  ]
}
```

---

### 3.4 Job Service — Port 8003

**Responsibility:** CRUD operations on job listings, keyword-based job search, skills tagging.

**Key Files:**
```
backend/job-service/
├── app/
│   ├── main.py
│   ├── models.py        # Job DB model
│   ├── schemas.py
│   ├── crud.py
│   └── database.py
└── requirements.txt
```

**Database Table: `jobs`**
```sql
CREATE TABLE jobs (
    id           SERIAL PRIMARY KEY,
    title        VARCHAR NOT NULL,
    company      VARCHAR,
    location     VARCHAR,
    description  TEXT,
    skills_req   TEXT[],           -- required skill tags
    salary_min   INTEGER,
    salary_max   INTEGER,
    posted_at    TIMESTAMP DEFAULT NOW()
);
```

**Endpoints:**
```
GET    /jobs/              → List all jobs (paginated)
GET    /jobs/{job_id}      → Get single job
POST   /jobs/              → Create job listing (admin)
DELETE /jobs/{job_id}      → Delete job (admin)
GET    /jobs/search?q=     → Keyword search on title/skills
```

---

### 3.5 Match Service — Port 8004

**Responsibility:** Compare user resume skills against job requirements. Produce a match score and ranked list.

**Key Files:**
```
backend/match-service/
├── app/
│   ├── main.py
│   ├── matcher.py       # Skill overlap scoring logic
│   ├── schemas.py
│   └── utils.py
└── requirements.txt
```

**Matching Algorithm:**
```python
def calculate_match_score(resume_skills: list, job_skills: list) -> float:
    matched = set(resume_skills) & set(job_skills)
    score = len(matched) / len(job_skills) * 100
    return round(score, 2)
```

**Endpoints:**
```
POST /match/              → Returns match score for resume vs job
POST /match/top-jobs/     → Returns top N matched jobs for a user
```

**Match Response:**
```json
{
  "job_id": 42,
  "match_score": 87.5,
  "matched_skills": ["Python", "FastAPI", "Docker"],
  "missing_skills": ["Kubernetes"]
}
```

---

### 3.6 Salary Service — Port 8005

**Responsibility:** ML-based salary prediction using job title, skills, location, and experience.

**Key Files:**
```
backend/salary-service/
├── app/
│   ├── main.py
│   ├── model.py         # Trained sklearn/XGBoost model loader
│   ├── predict.py       # Feature engineering + inference
│   ├── schemas.py
│   └── artifacts/
│       └── salary_model.pkl   # Serialized ML model
└── requirements.txt
```

**Endpoints:**
```
POST /salary/predict      → Returns salary range prediction
GET  /salary/benchmarks   → Aggregated salary data by role
```

**Request:**
```json
{
  "job_title": "Backend Developer",
  "skills": ["Python", "FastAPI", "PostgreSQL"],
  "location": "Bangalore",
  "experience_years": 2
}
```

**Response:**
```json
{
  "min_salary": 600000,
  "max_salary": 1200000,
  "median_salary": 850000,
  "currency": "INR"
}
```

---

### 3.7 Interview Service — Port 8006

**Responsibility:** Generate role-specific interview questions based on job title and skills using AI.

**Key Files:**
```
backend/interview-service/
├── app/
│   ├── main.py
│   ├── generator.py     # LLM prompt builder (Gemini / OpenAI)
│   ├── schemas.py
│   └── cache.py         # Redis caching of generated questions
└── requirements.txt
```

**Endpoints:**
```
POST /interview/generate   → Returns interview questions for role+skills
GET  /interview/questions  → Cached questions list
```

**Request:**
```json
{
  "job_title": "Full Stack Developer",
  "skills": ["React", "Node.js", "FastAPI"],
  "difficulty": "medium",
  "count": 10
}
```

**Response:**
```json
{
  "questions": [
    { "category": "Technical", "question": "Explain the React reconciliation algorithm." },
    { "category": "System Design", "question": "How would you design a scalable REST API?" }
  ]
}
```

---

### 3.8 Recommendation Service

**Responsibility:** Personalized job recommendations based on user history, resume, and behavior patterns.

**Key Files:**
```
backend/recommendation-service/
├── app/
│   ├── main.py
│   ├── recommender.py   # Collaborative / content-based filtering
│   └── schemas.py
└── requirements.txt
```

**Endpoints:**
```
GET  /recommendations/{user_id}   → Personalized job list
POST /recommendations/feedback    → Record user click/apply signals
```

---

## 4. Infrastructure Layer

### PostgreSQL — Port 5432

Each service has its own logical schema/database to maintain service independence.

| Service | Database Name |
|---|---|
| User Service | `jobiq_users` |
| Resume Service | `jobiq_resumes` |
| Job Service | `jobiq_jobs` |

### Redis — Port 6379

Used for:
- JWT token blacklisting (logout)
- Caching generated interview questions
- Caching salary benchmark data
- Session state

### Kafka — Port 9092

Used for async event propagation between services.

| Topic | Producer | Consumer |
|---|---|---|
| `user.registered` | User Service | Recommendation Service |
| `resume.uploaded` | Resume Service | Match Service |
| `job.applied` | Job Service | Recommendation Service |

### Zookeeper — Port 2181

Manages Kafka broker coordination.

---

## 5. API Contract Reference

### Authentication Header
All protected endpoints require:
```
Authorization: Bearer <JWT_TOKEN>
```

### Full Report Endpoint
Aggregates three services in one call (salary + interview + match):

**Request:**
```
POST /full-report
Content-Type: application/json
Authorization: Bearer <token>
```
```json
{
  "user_id": 1,
  "job_id": 42
}
```

**Response:**
```json
{
  "match": {
    "score": 87.5,
    "matched_skills": ["Python", "Docker"],
    "missing_skills": ["Kubernetes"]
  },
  "salary": {
    "min": 600000,
    "max": 1200000,
    "median": 850000
  },
  "interview": {
    "questions": [
      { "category": "Technical", "question": "..." }
    ]
  }
}
```

---

## 6. Inter-Service Communication

Services **never call each other directly**. All cross-service HTTP calls are routed via the API Gateway. For async tasks, Kafka events are used.

```
Frontend
  → API Gateway (HTTP)
    → Target Service (HTTP, internal)
      → Kafka (if async side-effect needed)
        → Consuming Service (processes event independently)
```

### Example: Resume Upload Flow
```
1. Frontend → POST /upload-resume/ → API Gateway
2. API Gateway → POST /parse/ → Resume Service
3. Resume Service → parses file → saves to DB
4. Resume Service → publishes `resume.uploaded` event to Kafka
5. Match Service (consumer) → fetches resume → runs match scoring
6. API Gateway → returns parse result to Frontend
```

---

## 7. Authentication & Security

- Passwords hashed with **bcrypt** before storage
- JWT tokens signed with **HS256**, expiry: 24 hours
- API Gateway validates JWT on every protected route before proxying
- Token blacklist stored in **Redis** (for logout/revoke support)

**JWT Verification Flow:**
```
Request → API Gateway
  → Extract Bearer token from Authorization header
  → Decode + verify signature with SECRET_KEY
  → Check token not in Redis blacklist
  → Extract user_id from sub claim
  → Attach user context to request
  → Proxy to target service
```

---

## 8. Database Design

All services use **SQLAlchemy ORM** with **PostgreSQL**. Migrations managed via **Alembic**.

### Core Entity Relationships

```
users (user-service)
  │
  ├── resumes (resume-service)
  │     └── skills[], experience[], education[]
  │
  └── job_applications (job-service)
        └── job_id → jobs table
```

### Connection Pattern (per service)
```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost:5432/jobiq_<service>"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 9. Kafka Event Streaming

### Producer (Resume Service)
```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

producer.send('resume.uploaded', {
    'user_id': user_id,
    'resume_id': resume.id,
    'skills': resume.skills
})
```

### Consumer (Match Service)
```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'resume.uploaded',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    data = message.value
    run_matching(data['user_id'], data['skills'])
```

---

## 10. Redis Caching Strategy

```python
import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Cache interview questions (TTL: 1 hour)
def get_or_generate_questions(job_title: str, skills: list):
    cache_key = f"interview:{job_title}:{','.join(sorted(skills))}"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    questions = generate_from_llm(job_title, skills)
    r.setex(cache_key, 3600, json.dumps(questions))
    return questions
```

---

## 11. Full Request Lifecycle

### Scenario: User logs in and gets job recommendations

```
Step 1: POST /users/login
  → API Gateway receives request
  → Proxies to User Service :8001
  → User Service verifies password (bcrypt compare)
  → Issues JWT token
  → Returns { access_token, token_type }

Step 2: GET /jobs/ (with Bearer token)
  → API Gateway validates JWT
  → Proxies to Job Service :8003
  → Job Service queries PostgreSQL
  → Returns paginated job list

Step 3: POST /full-report (with user_id + job_id)
  → API Gateway validates JWT
  → Calls Match Service :8004 → match score
  → Calls Salary Service :8005 → salary prediction
  → Calls Interview Service :8006 → questions (or Redis cache hit)
  → Aggregates all 3 responses
  → Returns combined JSON to frontend
```

---

## 12. Project Structure

```
jobiq/
├── backend/
│   ├── api-gateway/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── middleware.py
│   │   │   └── routers/
│   │   └── requirements.txt
│   │
│   ├── user-service/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── crud.py
│   │   │   ├── auth.py
│   │   │   └── database.py
│   │   └── requirements.txt
│   │
│   ├── resume-service/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── parser.py
│   │   │   ├── nlp.py
│   │   │   ├── models.py
│   │   │   └── database.py
│   │   └── requirements.txt
│   │
│   ├── job-service/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── models.py
│   │   │   ├── crud.py
│   │   │   └── database.py
│   │   └── requirements.txt
│   │
│   ├── match-service/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   └── matcher.py
│   │   └── requirements.txt
│   │
│   ├── salary-service/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── predict.py
│   │   │   └── artifacts/salary_model.pkl
│   │   └── requirements.txt
│   │
│   ├── interview-service/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── generator.py
│   │   │   └── cache.py
│   │   └── requirements.txt
│   │
│   └── recommendation-service/
│       ├── app/
│       │   ├── main.py
│       │   └── recommender.py
│       └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Login.jsx
│   │   │   └── Register.jsx
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   └── JobCard.jsx
│   │   ├── services/
│   │   │   └── api.js         # Axios instance + JWT interceptors
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── docker-compose.yml
├── start-all-services.bat
└── README.md
```

---

## 13. Environment Variables

Each service has its own `.env` file. Core variables:

### API Gateway `.env`
```env
SECRET_KEY=your_jwt_secret_key
USER_SERVICE_URL=http://localhost:8001
RESUME_SERVICE_URL=http://localhost:8002
JOB_SERVICE_URL=http://localhost:8003
MATCH_SERVICE_URL=http://localhost:8004
SALARY_SERVICE_URL=http://localhost:8005
INTERVIEW_SERVICE_URL=http:/