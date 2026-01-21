import unittest
import tempfile
import os
import pandas as pd
from employee_scraper.scraper import parse_file

class TestParsing(unittest.TestCase):

    def test_csv_file_parsing(self):
        with tempfile.TemporaryDirectory() as tmp:
            file_path = os.path.join(tmp, "employees.csv")

            with open(file_path, "w") as f:
                f.write(
                    "User ID,First Name,Last Name,sex,Email,Job Title,Phone Number\n"
                    "1,John,Doe,Male,john@example.com,Engineer,+1234567890"
                )

            df = parse_file(file_path)

            self.assertIsInstance(df, pd.DataFrame)
            self.assertEqual(len(df), 1)
            self.assertListEqual(
                list(df.columns),
                [
                    "User ID",
                    "First Name",
                    "Last Name",
                    "sex",
                    "Email",
                    "Job Title",
                    "Phone Number",
                ],
            )

    def test_unsupported_file_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            file_path = os.path.join(tmp, "data.txt")
            with open(file_path, "w") as f:
                f.write("invalid")

            with self.assertRaises(ValueError):
                parse_file(file_path)

if __name__ == "__main__":
    unittest.main()
