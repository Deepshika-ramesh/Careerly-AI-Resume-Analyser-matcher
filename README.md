Careerly — AI Resume Intelligence
Live demo: https://careerly-ai-resume-matcher.onrender.com/ui/
API documentation: https://careerly-ai-resume-matcher.onrender.com/docs
Source code: https://github.com/Deepshika-ramesh/Careerly-AI-Resume-Analyser-matcher

Careerly is a lightweight resume-to-job-description analysis web application. It helps a job seeker compare the skills in a PDF resume with the requirements in a job description, identify potential skill gaps, and get practical recommendations.
Important: Careerly is a decision-support tool, not an official Applicant Tracking System (ATS), hiring decision, or probability of getting shortlisted. Its scores are internal matching indicators.

Features
- Upload a PDF resume and extract its text.
- Identify technical skills using a configurable skill dictionary and aliases.
- Compare resume skills with skills mentioned in a job description.
- Show matched skills, missing skills, a match percentage, and recommendations.
- Calculate text similarity using TF-IDF vectors and cosine similarity.
- Use a browser interface with dark/light theme options.
- Export an analysis report as a text file.
- Expose a FastAPI backend and interactive API documentation.
- Include unit tests for skill extraction, aliases, partial-word matching, and match-percentage logic.
Live demo
Open Careerly and try a resume PDF with a job description. The free Render service may sleep after inactivity; the first request after sleeping can take longer to load.
Technology stack
- Language: Python
- API/backend: FastAPI, Uvicorn
- PDF extraction: pypdf
- Text matching: scikit-learn TF-IDF and cosine similarity
- Frontend: HTML, CSS, JavaScript
- Validation/testing: Python unittest
- Hosting: Render
- Version control: Git and GitHub
How it works
1. The user uploads a PDF resume and pastes a target job description.
2. The backend extracts text from the PDF.
3. The skill-matching logic identifies known skills and aliases in the resume and job description.
4. Careerly reports matching and missing skills and calculates a keyword-based match percentage.
5. TF-IDF vectorization represents the resume and job description as weighted word features; cosine similarity compares the vectors.
6. The interface displays scores, skill gaps, and recommendations, and can export a text report.
Why TF-IDF?
The initial transformer-based similarity approach was too resource-intensive for the free hosting memory limit. The current implementation uses TF-IDF and cosine similarity, which are lighter and easier to deploy. This is lexical/statistical text similarity, not an LLM or transformer-based semantic embedding model. Similar wording can increase the score; a high score does not guarantee a good candidate-role fit.
Run locally (Windows)
Prerequisites: Python installed and Git installed.
git clone https://github.com/Deepshika-ramesh/Careerly-AI-Resume-Analyser-matcher.git
cd Careerly-AI-Resume-Analyser-matcher

python -m venv venv
venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements.txt

python -m uvicorn app.main:app --port 8001
Open the frontend at http://127.0.0.1:8001/ui/
Open the API docs at http://127.0.0.1:8001/docs

To stop the server, return to the terminal and press Ctrl+C.
Run tests
From the repository root, with the virtual environment activated:
python -m unittest discover -s tests -v
The five existing unit tests cover:
- avoiding partial-word matches;
- match-percentage calculation;
- detection of multiple skills;
- handling a job description with no detected skills;
- recognition of skill aliases.
API endpoints
Method	Endpoint	Purpose
GET	/	Basic API health/message
POST	/analyze-job	Analyze skills in a job description
POST	/upload-resume	Upload/process a resume
POST	/match	Compare resume content with a job description
GET	/docs	Interactive Swagger API documentation
GET	/ui/	Browser interface


Check /docs for the current request fields and response schemas.
Deployment
The public demo is hosted on Render. The service runs independently of the developer's laptop and browser tabs. If the GitHub main branch is connected to Render with automatic deployment enabled, pushing a commit can trigger a new deployment.

Typical Render configuration:
- Build command: pip install -r requirements.txt
- Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Confirm the actual settings in the Render dashboard before changing them. Render's free web services can spin down after inactivity, and their local filesystem is ephemeral. Do not rely on the server's local filesystem to persist uploaded resumes or generated files.
Privacy and responsible use
- Test with sample or synthetic resumes where possible.
- Do not upload someone else's resume without permission.
- Do not use the match score as the sole basis for hiring or career decisions.
- Skill extraction depends on the skill list and aliases; unrecognized wording can be missed.
- PDF text extraction may fail on scanned/image-only PDFs.
- Treat recommendations as suggestions to investigate, not claims that the user has a skill.
Current limitations
- Skill recognition is dictionary/alias based and can miss context or unfamiliar terminology.
- TF-IDF similarity is based on word features; it does not deeply understand meaning.
- The match percentage is not an official ATS score and is not a hiring/shortlisting probability.
- The current app is not an LLM chatbot, RAG system, or agent.
- Scanned PDFs may require OCR, which is not currently described as a supported feature.
- Free hosting can have cold starts and limited resources.
Roadmap
- Add API-level tests for empty inputs, malformed PDFs, and invalid requests.
- Add a small, labeled evaluation set to assess score behavior.
- Improve skill normalization and show the evidence text behind each match.
- Add screenshots/GIF of the UI and a short demo walkthrough.
- Consider job-specific resume tailoring only after the current workflow and documentation are stable.
Project status
A working, publicly deployed portfolio project. The author has tested the core unit tests and adjusted the similarity approach to stay within free-hosting memory limits.