from unittest.mock import patch, Mock
from employee_scraper.scraper import download_file, parse_file
from employee_scraper.validator import validate_record

@patch("requests.get")
def test_file_download_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b"User ID,First Name,Last Name,sex,Email,Job Title,Phone Number"
    mock_response.headers = {"Content-Type": "text/csv"}

    mock_get.return_value = mock_response

    file_path = download_file("https://drive.google.com/uc?id=1AWPf-pJodJKeHsARQK_RHiNsE8fjPCVK&export=download")
    assert file_path.endswith(".csv")
