
import unittest

from app.main import extract_skills, compare_skills


class TestSkillMatching(unittest.TestCase):

    def test_detects_multiple_skills(self):
        text = "Python, FastAPI, Docker and PostgreSQL"
        skills = extract_skills(text)

        self.assertIn("python", skills)
        self.assertIn("fastapi", skills)
        self.assertIn("docker", skills)
        self.assertIn("postgresql", skills)

    def test_recognizes_skill_aliases(self):
        text = "We use sklearn, RESTful API and PowerBI"
        skills = extract_skills(text)

        self.assertIn("scikit-learn", skills)
        self.assertIn("rest api", skills)
        self.assertIn("power bi", skills)

    def test_avoids_partial_word_matches(self):
        skills = extract_skills("I enjoy JavaScript development")

        self.assertIn("javascript", skills)
        self.assertNotIn("java", skills)

    def test_calculates_match_percentage(self):
        result = compare_skills(
            ["python", "fastapi", "docker"],
            ["python", "fastapi", "postgresql", "docker"]
        )

        self.assertEqual(result["match_percentage"], 75.0)
        self.assertEqual(
            set(result["matched_skills"]),
            {"python", "fastapi", "docker"}
        )
        self.assertEqual(result["missing_skills"], ["postgresql"])

    def test_handles_empty_job_skills(self):
        result = compare_skills(["python"], [])

        self.assertEqual(result["match_percentage"], 0)
        self.assertEqual(result["missing_skills"], [])


if __name__ == "__main__":
    unittest.main()
