from fastapi import FastAPI, UploadFile, File, Form
from pypdf import PdfReader
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount(
    "/ui",
    StaticFiles(directory="frontend", html=True),
    name="ui"
)
model = SentenceTransformer("all-MiniLM-L6-v2")


SKILLS = [
    "python",
    "java",
    "javascript",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "fastapi",
    "streamlit",
    "pandas",
    "openpyxl",
    "docker",
    "machine learning",
    "aws",
    "git",
    "react",
    "rest api",
    "etl",
    "power bi"
]


SKILL_RECOMMENDATIONS = {
    "python": "Practise functions, data structures, exception handling, OOP, and coding problems.",
    "sql": "Practise JOINs, GROUP BY, HAVING, subqueries, and query optimisation.",
    "fastapi": "Build CRUD endpoints and practise request validation, error handling, and API testing.",
    "docker": "Learn Dockerfiles, images, containers, and how to containerise a Python API.",
    "aws": "Learn core AWS services and practise deploying a small application.",
    "git": "Practise branches, commits, pull requests, and resolving merge conflicts.",
    "machine learning": "Build a small machine learning project and evaluate its performance.",
    "pandas": "Practise cleaning, merging, grouping, and analysing real datasets.",
    "mongodb": "Practise CRUD operations, indexes, data modelling, and Python integration.",
    "postgresql": "Practise database design, joins, indexes, and connecting Python to PostgreSQL.",
    "mysql": "Practise SQL queries, joins, constraints, and database design.",
    "react": "Build reusable components, manage state, and connect your app to an API.",
    "javascript": "Practise asynchronous JavaScript, DOM manipulation, and API integration.",
    "rest api": "Practise REST endpoint design, HTTP status codes, and request/response schemas.",
    "etl": "Build a pipeline that extracts, transforms, validates, and loads a dataset.",
    "power bi": "Build a dashboard using data transformations, relationships, and measures.",
    "openpyxl": "Practise reading, editing, formatting, and validating Excel workbooks.",
    "streamlit": "Build a small data app with file uploads and interactive forms.",
    "java": "Review OOP, collections, exception handling, and data structures."
}

def extract_skills(text):
    found_skills = []
    text = text.lower()

    for skill in SKILLS:
        pattern = rf"\b{re.escape(skill.lower())}\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


def compare_skills(resume_skills, job_skills):
    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched_skills = sorted(resume_set & job_set)
    missing_skills = sorted(job_set - resume_set)

    if len(job_set) > 0:
        match_percentage = round(
            len(matched_skills) / len(job_set) * 100,
            2
        )
    else:
        match_percentage = 0

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage
    }


def generate_recommendations(missing_skills):
    recommendations = []

    for skill in missing_skills:
        suggestion = SKILL_RECOMMENDATIONS.get(
            skill,
            f"Learn the fundamentals of {skill} and practise with a small project."
        )

        recommendations.append({
            "skill": skill,
            "recommendation": suggestion
        })

    return recommendations


def calculate_semantic_similarity(resume_text, job_description):
    embeddings = model.encode([
        resume_text,
        job_description
    ])

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(float(similarity) * 100, 2)

@app.get("/")
def home():
    return {
        "message": "AI Job Intelligence API is running!"
    }


@app.post("/analyze-job")
def analyze_job(job_description: str):

    found_skills = extract_skills(job_description)

    return {
        "word_count": len(job_description.split()),
        "skills_found": found_skills
    }


@app.post("/upload-resume")
def upload_resume(file: UploadFile = File(...)):

    reader = PdfReader(file.file)

    resume_text = ""

    for page in reader.pages:
        resume_text += page.extract_text() or ""

    resume_skills = extract_skills(resume_text)

    return {
        "filename": file.filename,
        "skills_found": resume_skills,
        "text": resume_text
    }


@app.post("/match")
def match_resume_to_job(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):

    reader = PdfReader(resume.file)

    resume_text = ""

    for page in reader.pages:
        resume_text += page.extract_text() or ""

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    comparison = compare_skills(
        resume_skills,
        job_skills
    )

    semantic_score = calculate_semantic_similarity(
    resume_text,
    job_description
)

    
    recommendations = generate_recommendations(
        comparison["missing_skills"]
    )

    return {
    "resume_filename": resume.filename,
    "job_skills": sorted(job_skills),
    **comparison,
    "recommendations": generate_recommendations(
        comparison["missing_skills"]
    ),
    "semantic_similarity": semantic_score
}