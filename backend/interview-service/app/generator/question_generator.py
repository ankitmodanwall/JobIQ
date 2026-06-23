def generate_questions(role, skills):
    # Base behavioral questions
    questions = [
        f"Tell me about a time you solved a complex problem as a {role}.",
        "How do you handle tight deadlines and high-pressure situations?"
    ]
    
    # Technical questions based on the skills extracted from your resume
    skill_questions = {
        "python": "What is the difference between deep copy and shallow copy in Python?",
        "sql": "Explain the difference between a WHERE clause and a HAVING clause.",
        "java": "What are the main principles of Object-Oriented Programming (OOP)?",
        "react": "What are React Hooks, and how do they change how we build components?",
        "fastapi": "How does FastAPI use Pydantic for data validation?"
    }
    
    # Match the user's skills with our question database
    for skill in skills:
        s_lower = skill.lower().strip()
        if s_lower in skill_questions:
            questions.append(skill_questions[s_lower])
            
    return questions