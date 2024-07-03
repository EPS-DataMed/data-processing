import unittest
from unittest.mock import MagicMock
from datetime import datetime
from starlette.responses import JSONResponse

from app.scraping import data_scraping, DataScraped, extract_text_from_s3_pdf

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

if __name__ == '__main__':
    unittest.main()