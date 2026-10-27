
import unittest
from fastapi.testclient import TestClient
from io import BytesIO
from pypdf import PdfWriter
from io import BytesIO
from reportlab.pdfgen import canvas

from app.main import app


client = TestClient(app)


class TestCareerlyAPI(unittest.TestCase):

    
    def test_upload_resume_valid_pdf(self):
        pdf_buffer = BytesIO()
        writer = PdfWriter()
        writer.add_blank_page(width=300, height=300)
        writer.write(pdf_buffer)
        pdf_buffer.seek(0)

        response = client.post(
            "/upload-resume",
            files={
                "file": (
                    "sample_resume.pdf",
                    pdf_buffer,
                    "application/pdf"
                )
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["filename"], "sample_resume.pdf")
        self.assertIn("skills_found", data)
        self.assertIn("text", data)


    def test_analyze_job_missing_description(self):
        response = client.post("/analyze-job")

        self.assertEqual(response.status_code, 422)

    def test_upload_resume_missing_file(self):
        response = client.post("/upload-resume")

        self.assertEqual(response.status_code, 422)

    def test_match_missing_resume_and_description(self):
        response = client.post("/match")

        self.assertEqual(response.status_code, 422)

    def test_match_missing_resume(self):
        response = client.post(
            "/match",
            data={"job_description": "Python developer with SQL skills"}
        )

        self.assertEqual(response.status_code, 422)

    def test_match_missing_job_description(self):
        response = client.post(
            "/match",
            files={
                "resume": (
                    "resume.pdf",
                    b"dummy PDF content",
                    "application/pdf"
                )
            }
        )

        self.assertEqual(response.status_code, 422)

        
    def test_analyze_job_empty_description(self):
        response = client.post(
            "/analyze-job",
            params={"job_description": ""}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["word_count"], 0)
        self.assertEqual(response.json()["skills_found"], [])

    def test_analyze_job_valid_description(self):
        response = client.post(
            "/analyze-job",
            params={
                "job_description": "Python developer with SQL skills"
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("word_count", data)
        self.assertIn("skills_found", data)
        self.assertIn("python", data["skills_found"])
        self.assertIn("sql", data["skills_found"])

    def test_home_endpoint(self):
        response = client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["message"],
            "AI Job Intelligence API is running!"
        )

        
    def test_match_valid_resume_and_job_description(self):
        pdf_buffer = BytesIO()

        pdf = canvas.Canvas(pdf_buffer)
        pdf.drawString(
            50, 750,
            "Python developer with SQL, FastAPI, and Git experience."
        )
        pdf.save()
        pdf_buffer.seek(0)

        response = client.post(
            "/match",
            data={
                "job_description":
                    "Python developer with SQL and FastAPI skills"
            },
            files={
                "resume": (
                    "sample_resume.pdf",
                    pdf_buffer,
                    "application/pdf"
                )
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIsInstance(data, dict)
        self.assertTrue(len(data) > 0)




if __name__ == "__main__":
    unittest.main()
