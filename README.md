# Careerly — AI Resume Intelligence

Careerly is a Python-based resume analysis application that compares a candidate's resume with a target job description. It identifies matching skills, highlights skill gaps, calculates semantic similarity, and provides actionable learning recommendations.

## Features

- **PDF Resume Parsing:** Extracts text from uploaded PDF resumes.
- **Skill Extraction:** Identifies technical skills using a configurable skill dictionary and aliases.
- **Keyword Matching:** Calculates overlap between detected resume and job-description skills.
- **Semantic Similarity:** Uses Sentence Transformers to compare resume and job-description text.
- **Skill Gap Analysis:** Highlights missing skills and suggests practical next steps.
- **Downloadable Reports:** Exports analysis results as a text file.
- **Responsive Interface:** Includes dark and light themes.

## Tech Stack

- Python
- FastAPI
- Sentence Transformers (`all-MiniLM-L6-v2`)
- scikit-learn
- PyPDF
- HTML, CSS and JavaScript
- unittest

## Run Locally

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies.
4. Start the FastAPI server.

```bash
python -m venv venv
```

On Windows CMD:

```cmd
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8001
```

Open the application at `http://127.0.0.1:8001/ui/`.

## Run Tests

```cmd
python -m unittest discover -s tests -v
```

## How It Works

1. Upload a PDF resume.
2. Paste a target job description.
3. Careerly extracts skills from both documents.
4. The application calculates keyword overlap and semantic similarity.
5. It displays matching skills, skill gaps, and recommendations.

## Limitations

- Skill extraction depends on the configured skill dictionary and aliases.
- Semantic similarity is a text-similarity measure, not a hiring probability.
- The keyword score is not an official ATS score.
- PDF text extraction may not work reliably with scanned documents.

## Future Improvements

- More robust skill normalization and contextual extraction.
- Automated API tests and validation.
- Docker support and deployment.
- Improved job-specific skill prioritization.

---

**Project status:** Working local prototype; ongoing improvements planned.
