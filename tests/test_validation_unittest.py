import unittest
from employee_scraper.validator import validate_record

class TestValidation(unittest.TestCase):

    def test_valid_record(self):
        record = {
            "User ID": 1,
            "First Name": "Jane",
            "Last Name": "Doe",
            "sex": "Female",
            "Email": "jane@example.com",
            "Job Title": "Manager",
            "Phone Number": "+1234567890",
        }

        errors = validate_record(record)
        self.assertEqual(errors, [])

    def test_invalid_record(self):
        record = {
            "User ID": None,
            "First Name": "Jane",
            "Last Name": "",
            "sex": "Alien",
            "Email": "invalid-email",
            "Job Title": "",
            "Phone Number": "12345",
        }

        errors = validate_record(record)
        self.assertEqual(len(errors), 6)

if __name__ == "__main__":
    unittest.main()
