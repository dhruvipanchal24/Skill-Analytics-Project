role_skills = {
    "Data Analyst": ["python", "pandas", "numpy", "excel", "sql"],
    "Web Developer": ["html", "css", "javascript", "react"],
    "Backend Developer": ["django", "flask", "api", "database"],
    "ML Engineer": ["python", "machine learning", "numpy", "sklearn"],
    "Database Administratr":["sql","mysql","mongodb","postgresql","backup","security"],
}

def recommend_skills(user_text, role):
    user_skills = user_text.lower().replace(",", " ").split()
    required = role_skills.get(role, [])

    missing = list(set(required) - set(user_skills))
    return missing