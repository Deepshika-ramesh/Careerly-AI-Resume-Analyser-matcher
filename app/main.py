from fastapi import FastAPI, UploadFile, File, Form
from pypdf import PdfReader
import re
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount(
    "/ui",
    StaticFiles(directory="frontend", html=True),
    name="ui"
)
model = None


SKILLS = [
    # Programming languages
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    "go",
    "r",

    # Databases and querying
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "sqlite",
    "redis",
    "database design",

    # Backend and APIs
    "fastapi",
    "flask",
    "django",
    "streamlit",
    "rest api",
    "graphql",
    "microservices",

    # Data analysis and engineering
    "pandas",
    "numpy",
    "openpyxl",
    "etl",
    "data analysis",
    "data visualization",
    "data cleaning",
    "data engineering",
    "excel",
    "power bi",
    "tableau",
    "apache spark",
    "apache kafka",
    "airflow",

    # Machine learning and AI
    "machine learning",
    "deep learning",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "keras",
    "natural language processing",
    "computer vision",
    "generative ai",
    "large language models",
    "prompt engineering",
    "retrieval augmented generation",
    "langchain",
    "hugging face",
    "vector databases",
    "chromadb",
    "faiss",
    "openai api",
    "azure openai",
    "yolo",

    # Cloud and DevOps
    "aws",
    "azure",
    "google cloud",
    "docker",
    "kubernetes",
    "jenkins",
    "git",
    "github",
    "linux",
    "ci/cd",

    # Frontend and web
    "html",
    "css",
    "react",
    "next.js",

    # Testing and development practices
    "pytest",
    "unit testing",
    "integration testing",
    "object-oriented programming",
    "data structures",
    "algorithms",
    "agile",
]


SKILL_ALIASES = {
    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "restful api": "rest api",
    "restful apis": "rest api",
    "rest apis": "rest api",
    "retrieval-augmented generation": "retrieval augmented generation",
    "rag pipeline": "retrieval augmented generation",
    "powerbi": "power bi",
    "ci cd": "ci/cd",
    "large language model": "large language models",
    "llms": "large language models",
    "postgres": "postgresql",
}


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
    text = text.lower()
    found_skills = set()

    for skill in SKILLS:
        pattern = rf"(?<!\w){re.escape(skill.lower())}(?!\w)"

        if re.search(pattern, text):
            found_skills.add(skill)

    for alias, canonical_skill in SKILL_ALIASES.items():
        pattern = rf"(?<!\w){re.escape(alias)}(?!\w)"

        if re.search(pattern, text):
            found_skills.add(canonical_skill)

    return sorted(found_skills)


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
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    vectorizer = TfidfVectorizer(stop_words="english")

    try:
        vectors = vectorizer.fit_transform([
            resume_text,
            job_description
        ])

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]

        return round(float(similarity) * 100, 2)

    except ValueError:
        return 0.0

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