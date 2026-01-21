import unittest
from unittest.mock import patch, Mock
from employee_scraper.scraper import download_file

class TestFileDownload(unittest.TestCase):

    @patch("employee_scraper.scraper.requests.Session.get")
    def test_csv_file_download_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {
            "Content-Disposition": "attachment; filename=employee.csv"
        }
        mock_response.iter_content.return_value = [
            b"User ID,First Name,Last Name,sex,Email,Job Title,Phone Number"
        ]
        mock_response.raise_for_status.return_value = None
        mock_response.cookies = {}

        mock_get.return_value = mock_response

        file_path = download_file("http://fake-url.com/file")

        self.assertTrue(file_path.endswith(".csv"))

if __name__ == "__main__":
    unittest.main()
