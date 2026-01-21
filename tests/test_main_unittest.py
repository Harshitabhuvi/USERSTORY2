import unittest
from unittest.mock import patch
from employee_scraper import main

class TestMainExecution(unittest.TestCase):

    @patch("employee_scraper.main.process_employee_data")
    @patch("employee_scraper.main.parse_file")
    @patch("employee_scraper.main.download_file")
    def test_main_runs_successfully(
        self,
        mock_download,
        mock_parse,
        mock_process
    ):
        # Arrange (mock behavior)
        mock_download.return_value = "employee_data.csv"
        mock_parse.return_value = []   # fake dataframe
        mock_process.return_value = ([], [])

        # Act
        main.main()

        # Assert
        mock_download.assert_called_once()
        mock_parse.assert_called_once()
        mock_process.assert_called_once()
