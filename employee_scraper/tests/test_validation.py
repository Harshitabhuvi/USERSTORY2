from employee_scraper.validator import validate_record
from employee_scraper.scraper import download_file, parse_file


def test_valid_record():
    record = {
        "User ID": 1,
        "First Name": "Jane",
        "Last Name": "Doe",
        "sex": "Female",
        "Email": "jane@example.com",
        "Job Title": "Manager",
        "Phone Number": "+1234567890"
    }

    errors = validate_record(record)
    assert errors == []

def test_invalid_record():
    record = {
        "User ID": None,
        "First Name": "Jane",
        "Last Name": "",
        "sex": "Alien",
        "Email": "invalid-email",
        "Job Title": "",
        "Phone Number": "12345"
    }

    errors = validate_record(record)
    assert len(errors) == 6  # Missing/invalid fields
