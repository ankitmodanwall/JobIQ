from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from app import models, schemas, database
from app.kafka_producer import send_user_event

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Password hashing
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

# JWT Configuration
SECRET_KEY = "ankit-job-platform-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI(title="User Service")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# ✅ HEALTH CHECK
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "user-service"}


@app.get("/")
def read_root():
    return {
        "message": "User Service is up and running!"
    }


@app.post("/users/", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(database.get_db)
):
    db_user = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(user.password)

    new_user = models.User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Send Kafka Event
    send_user_event({
        "user_id": new_user.id,
        "email": new_user.email,
        "full_name": new_user.full_name
    })

    return new_user


@app.get("/users/")
def get_all_users(
    db: Session = Depends(database.get_db)
):
    return db.query(models.User).all()


@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(database.get_db)
):
    user = (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# ✅ FIXED: Login with user object
@app.post("/login")
def login(
    user: schemas.UserLogin,
    db: Session = Depends(database.get_db)
):
    db_user = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not pwd_context.verify(
        user.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {
            "sub": db_user.email,
            "user_id": db_user.id
        }
    )

    # ✅ FIX: User object return karo
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "full_name": db_user.full_name,
            "is_active": db_user.is_active
        }
    }