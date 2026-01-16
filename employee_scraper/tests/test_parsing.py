import pytest
import pandas as pd
from employee_scraper.scraper import parse_file, download_file
from employee_scraper.validator import validate_record
from employee_scraper.config import SUPPORTED_FORMATS

def test_csv_parsing(tmp_path):
    csv_file = tmp_path / "employees.csv"
    csv_file.write_text(
        "User ID,First Name,Last Name,sex,Email,Job Title,Phone Number\n"
        "1,John,Doe,Male,john@example.com,Engineer,+1234567890"
    )

    df = parse_file(str(csv_file))
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert list(df.columns) == [
        "User ID",
        "First Name",
        "Last Name",
        "sex",
        "Email",
        "Job Title",
        "Phone Number"
    ]

def test_unsupported_file_format(tmp_path):
    # Test Case 3: Validate File Type and Format
    fake_file = tmp_path / "data.txt"  # unsupported extension
    fake_file.write_text("Some content")

    with pytest.raises(ValueError) as exc_info:
        parse_file(str(fake_file))

    assert "Unsupported file format" in str(exc_info.value)
