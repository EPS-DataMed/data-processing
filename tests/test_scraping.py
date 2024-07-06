import unittest
from unittest.mock import MagicMock
from datetime import datetime
from starlette.responses import JSONResponse

from app.scraping import (
    data_scraping, DataScraped, extract_text_from_s3_pdf,
    extract_values_from_text, extract_test_date, extract_data_and_date, text_processing
)

class TestScrapingFunctions(unittest.TestCase):

    def setUp(self):
        # Mocking AWS S3 client
        self.mock_s3_client = MagicMock()
        self.mock_s3_client.get_object.return_value = {
            'Body': MagicMock(return_value=b"Mock PDF content")
        }

    def test_extract_text_from_s3_pdf(self):
        # Simulate AWS S3 response
        user_id = 1
        filename = "example.pdf"
        expected_text = "Mock PDF content"

        # Mock return value for extract_text_from_s3_pdf
        with unittest.mock.patch.dict('os.environ', {'S3_BUCKET_NAME': 'mock-bucket'}):
            with unittest.mock.patch('app.scraping.s3_client', self.mock_s3_client):
                # Modificando o mock para retornar diretamente a string
                with unittest.mock.patch('app.scraping.extract_text_from_s3_pdf', return_value=expected_text):
                    extracted_text = extract_text_from_s3_pdf(user_id, filename)
                    if isinstance(extracted_text, JSONResponse):
                        self.assertEqual(extracted_text.status_code, 500)
                        self.assertIn("Error while downloading the file", extracted_text.body.decode())
                    else:
                        self.assertIsInstance(extracted_text, str)
                        self.assertEqual(extracted_text, expected_text)

    def test_data_scraping(self):
        user_id = 1
        filename = "example.pdf"

        # Mock return value for extract_text_from_s3_pdf
        with unittest.mock.patch.dict('os.environ', {'S3_BUCKET_NAME': 'mock-bucket'}):
            with unittest.mock.patch('app.scraping.s3_client', self.mock_s3_client):
                # Mantendo o mock anterior para test_data_scraping
                with unittest.mock.patch('app.scraping.extract_text_from_s3_pdf', return_value="Mock PDF content"):
                    extracted_data, extracted_date = data_scraping(user_id, filename)
                    self.assertIsInstance(extracted_data, list)
                    self.assertTrue(all(isinstance(data, DataScraped) for data in extracted_data))
                    self.assertIsInstance(extracted_date, (datetime, type(None)))

    def test_extract_values_from_text(self):
        text = """
        HEMOGLOBINA 13.5 g/dL
        HEMATÓCRITO 40.5 %
        HEMÁCIAS 4.7 milhões/mm3
        HEMOGLOBINA GLICADA - HbA1c RESULTADO: 5.6 %
        TRANSAMINASE OXALACÉTICA TGO (AST) RESULTADO: 30 U/L
        TRANSAMINASE PIRÚVICA TGP (ALT) RESULTADO: 25 U/L
        UREIA RESULTADO: 40 mg/dL
        CREATININA RESULTADO: 1.1 mg/dL
        """
        patterns = {
            "hemoglobin": (r'HEMOGLOBINA\s*([\d,\.]+)\s*g/dL', "g/dL"),
            "hematocrit": (r'HEMATÓCRITO\s*([\d,\.]+)\s*%', "%"),
            "red_blood_cell": (r'HEMÁCIAS\s*([\d,\.]+)\s*milhões/mm3', "milhões/mm3"),
            "glycated_hemoglobin": (r'HEMOGLOBINA GLICADA - HbA1c\s*.*?RESULTADO:\s*([\d,\.]+)\s*%', "%"),
            "ast": (r'TRANSAMINASE OXALACÉTICA TGO \(AST\).*?RESULTADO:\s*([\d,\.]+)\s*U/L', "U/L"),
            "alt": (r'TRANSAMINASE PIRÚVICA TGP \(ALT\).*?RESULTADO:\s*([\d,\.]+)\s*U/L', "U/L"),
            "urea": (r'UREIA\s*.*?RESULTADO:\s*([\d,\.]+)\s*mg/dL', "mg/dL"),
            "creatinine": (r'CREATININA\s*.*?RESULTADO:\s*([\d,\.]+)\s*mg/dL', "mg/dL")
        }
        expected_results = [
            DataScraped("hemoglobin", "13.5"),
            DataScraped("hematocrit", "40.5"),
            DataScraped("red_blood_cell", "4.7"),
            DataScraped("glycated_hemoglobin", "5.6"),
            DataScraped("ast", "30"),
            DataScraped("alt", "25"),
            DataScraped("urea", "40"),
            DataScraped("creatinine", "1.1")
        ]

        results = extract_values_from_text(text, patterns)
        self.assertEqual(len(results), len(expected_results))
        for result, expected in zip(results, expected_results):
            self.assertEqual(result.name, expected.name)
            self.assertEqual(result.value, expected.value)

    def test_extract_test_date(self):
        text = "Atendimento : 01/01/2023"
        expected_date = datetime(2023, 1, 1)
        extracted_date = extract_test_date(text)
        self.assertEqual(extracted_date, expected_date)

        text_no_date = "Atendimento : N/A"
        extracted_date = extract_test_date(text_no_date)
        self.assertIsNone(extracted_date)

    def test_extract_data_and_date(self):
        text = """
        Atendimento : 01/01/2023
        HEMOGLOBINA 13.5 g/dL
        HEMATÓCRITO 40.5 %
        HEMÁCIAS 4.7 milhões/mm3
        HEMOGLOBINA GLICADA - HbA1c RESULTADO: 5.6 %
        TRANSAMINASE OXALACÉTICA TGO (AST) RESULTADO: 30 U/L
        TRANSAMINASE PIRÚVICA TGP (ALT) RESULTADO: 25 U/L
        UREIA RESULTADO: 40 mg/dL
        CREATININA RESULTADO: 1.1 mg/dL
        """
        data_values, test_date = extract_data_and_date(text)
        
        expected_date = datetime(2023, 1, 1)
        expected_results = [
            DataScraped("hemoglobin", "13.5"),
            DataScraped("hematocrit", "40.5"),
            DataScraped("red_blood_cell", "4.7"),
            DataScraped("glycated_hemoglobin", "5.6"),
            DataScraped("ast", "30"),
            DataScraped("alt", "25"),
            DataScraped("urea", "40"),
            DataScraped("creatinine", "1.1")
        ]
        
        self.assertEqual(test_date, expected_date)
        self.assertEqual(len(data_values), len(expected_results))
        for result, expected in zip(data_values, expected_results):
            self.assertEqual(result.name, expected.name)
            self.assertEqual(result.value, expected.value)

    def test_text_processing(self):
        text = """
        Atendimento : 01/01/2023
        HEMOGLOBINA 13.5 g/dL
        HEMATÓCRITO 40.5 %
        HEMÁCIAS 4.7 milhões/mm3
        HEMOGLOBINA GLICADA - HbA1c RESULTADO: 5.6 %
        TRANSAMINASE OXALACÉTICA TGO (AST) RESULTADO: 30 U/L
        TRANSAMINASE PIRÚVICA TGP (ALT) RESULTADO: 25 U/L
        UREIA RESULTADO: 40 mg/dL
        CREATININA RESULTADO: 1.1 mg/dL
        """
        data_values, test_date = text_processing(text)
        
        expected_date = datetime(2023, 1, 1)
        expected_results = [
            DataScraped("hemoglobin", "13.5"),
            DataScraped("hematocrit", "40.5"),
            DataScraped("red_blood_cell", "4.7"),
            DataScraped("glycated_hemoglobin", "5.6"),
            DataScraped("ast", "30"),
            DataScraped("alt", "25"),
            DataScraped("urea", "40"),
            DataScraped("creatinine", "1.1")
        ]
        
        self.assertEqual(test_date, expected_date)
        self.assertEqual(len(data_values), len(expected_results))
        for result, expected in zip(data_values, expected_results):
            self.assertEqual(result.name, expected.name)
            self.assertEqual(result.value, expected.value)