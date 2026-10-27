# Careerly — AI Resume Intelligence

**Analyze your resume against a job description, identify skill gaps, and get actionable recommendations.**

[Live Demo](https://careerly-ai-resume-matcher.onrender.com/ui/) · [API Documentation](https://careerly-ai-resume-matcher.onrender.com/docs) · [GitHub Repository](https://github.com/Deepshika-ramesh/Careerly-AI-Resume-Analyser-matcher)

Careerly is a lightweight resume-to-job-description analysis web application built with Python and FastAPI. It extracts text from PDF resumes, compares candidate skills with job requirements, highlights missing skills, and generates recommendations to help job seekers identify areas for improvement.

**Important:** Careerly is a decision-support tool, not an official Applicant Tracking System (ATS), hiring decision, or predictor of shortlisting probability.

## Screenshots

### Backend

![Careerly backend](screenshots/Screenshot%202026-10-27%20170400.png)

### Application Interface

![Careerly application interface](screenshots/Screenshot%202026-10-27%20165906.png)

![Careerly application interface](screenshots/Screenshot%202026-10-27%20165928.png)

### Resume Analysis Results

![Careerly resume analysis results](screenshots/Screenshot%202026-10-27%20165944.png)

### Downloadable Analysis Report

![Careerly downloadable report](screenshots/Screenshot%202026-10-27%20170036.png)

## Features

- **PDF Resume Parsing:** Extract text from uploaded PDF resumes using `pypdf`.
- **Skill Extraction:** Identify technical skills using a configurable dictionary and aliases.
- **Skill Matching:** Compare resume skills with job description requirements.
- **Skill Gap Analysis:** Display matched skills, missing skills, and practical recommendations.
- **Match Percentage:** Calculate a keyword-based match score from detected job requirements.
- **Text Similarity:** Compare resume and job description text using TF-IDF and cosine similarity.
- **Web Interface:** Analyze resumes through a browser-based UI with dark and light themes.
- **Report Export:** Download the analysis report as a text file.
- **REST API:** Access the application's functionality through FastAPI endpoints.
- **Automated Tests:** Validate core matching logic and API behavior using Python's `unittest`.

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Backend and API | FastAPI, Uvicorn |
| PDF extraction | pypdf |
| Text similarity | scikit-learn, TF-IDF, cosine similarity |
| Frontend | HTML, CSS, JavaScript |
| Testing | unittest, FastAPI TestClient, httpx |
| Hosting | Render |
| Version control | Git, GitHub |

## How It Works

1. The user uploads a PDF resume and enters a target job description.
2. The backend extracts readable text from the PDF.
3. Careerly identifies recognized skills in the resume and job description.
4. The skill-matching logic calculates matched skills, missing skills, and a keyword-based match percentage.
5. TF-IDF vectorization converts the text into weighted word features, and cosine similarity compares the resulting vectors.
6. The interface presents the analysis, recommendations, and an option to download the report.

## Why TF-IDF Instead of Transformers?

The initial transformer-based similarity approach was too resource-intensive for the memory limits of the free hosting environment. I switched to TF-IDF and cosine similarity to reduce resource consumption and make deployment more practical.

TF-IDF provides lightweight, statistical text similarity based on word features. It is **not** an LLM-based system or a transformer-based semantic embedding model. Similar wording can increase the similarity score, and a high score does not guarantee that a candidate is suitable for a role.

## Live Demo

Try Careerly using a sample PDF resume and a job description.

- **Application:** [Open Careerly](https://careerly-ai-resume-matcher.onrender.com/ui/)
- **API documentation:** [Explore the API](https://careerly-ai-resume-matcher.onrender.com/docs)

The free Render service may spin down after inactivity, so the first request can take longer to complete.

## Run Locally on Windows

### Prerequisites

- Python installed
- Git installed

### 1. Clone the repository

```bash
git clone https://github.com/Deepshika-ramesh/Careerly-AI-Resume-Analyser-matcher.git
cd Careerly-AI-Resume-Analyser-matcher
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the application

```bash
python -m uvicorn app.main:app --port 8001
```

Open these URLs in your browser:

- **Web interface:** [http://127.0.0.1:8001/ui/](http://127.0.0.1:8001/ui/)
- **API documentation:** [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

To stop the server, press `Ctrl+C` in the terminal.

## Running Tests

Activate your virtual environment and run the following command from the repository root:

```bash
python -m unittest discover -s tests -v
```

**Latest reported result: 15 tests passed.**

The test suite covers:

- Skill matching and match-percentage calculation.
- Detection of multiple skills and skill aliases.
- Prevention of partial-word matches.
- Handling job descriptions with no detected skills.
- API validation for missing required inputs.
- Empty and valid job description analysis.
- The API health endpoint.
- PDF upload and response structure.
- Resume-to-job matching with a sample PDF.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API health/message |
| POST | `/analyze-job` | Extract recognized skills from a job description |
| POST | `/upload-resume` | Upload and process a PDF resume |
| POST | `/match` | Compare a resume with a job description |
| GET | `/docs` | Interactive Swagger API documentation |
| GET | `/ui/` | Browser interface |

Refer to `/docs` for the current request parameters, required fields, and response schemas.

## Deployment

Careerly is deployed on Render and connected to its GitHub source repository.

**Typical build command**

```bash
pip install -r requirements.txt
```

**Typical start command**

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Confirm the actual configuration in the Render dashboard before making changes. If automatic deployment is enabled for the connected GitHub branch, pushing a commit can trigger a new deployment.

Render's free services may spin down after inactivity, and their local filesystem is ephemeral. The application should not rely on local server storage for persistent resume uploads or reports.

## Privacy and Responsible Use

- Prefer sample or synthetic resumes when testing.
- Do not upload another person's resume without permission.
- Do not use the match percentage as the sole basis for hiring or career decisions.
- Skill extraction depends on the configured dictionary and aliases.
- Recommendations are suggestions to investigate, not proof that someone possesses a particular skill.
- Scanned or image-only PDFs may not produce readable text because OCR is not currently supported as a documented feature.

## Current Limitations

- Dictionary-based skill extraction may miss unfamiliar terminology or contextual meaning.
- TF-IDF measures text similarity rather than deep semantic understanding.
- The match percentage is not an official ATS score or a probability of getting shortlisted.
- Careerly is not an LLM chatbot, RAG system, or autonomous AI agent.
- Scanned PDFs may require OCR support.
- Free hosting can introduce cold starts and resource constraints.

## Future Improvements

- Build a labeled evaluation dataset to assess score quality.
- Improve skill normalization and display evidence supporting each detected match.
- Add malformed-PDF and additional edge-case tests.
- Explore job-specific resume tailoring after the existing workflow is stable.
- Add a short product demonstration video.

## Project Status

**Working, publicly deployed portfolio project.**

Careerly demonstrates Python development, REST API design, PDF processing, text analysis, automated testing, and deployment. The implementation prioritizes lightweight text similarity to remain practical within free-hosting resource constraints.