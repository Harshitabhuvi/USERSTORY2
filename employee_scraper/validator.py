# validator.py
import re
from employee_scraper.config import REQUIRED_FIELDS

EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"
PHONE_REGEX = r"^\+?\d{7,15}$"

def validate_record(record: dict) -> list:
    """
    Strict validation: checks required fields, email, phone, and sex.
    """
    errors = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        value = record.get(field)
        if value is None or str(value).strip() == "":
            errors.append(f"Missing field: {field}")

    # Validate email
    email = record.get("Email")
    if email and not re.match(EMAIL_REGEX, str(email).strip(), re.IGNORECASE):
        errors.append("Invalid email format")

    # Validate phone
    phone = record.get("Phone Number")
    if phone:
        phone_clean = str(phone).replace(" ", "").replace("-", "")
        if not re.match(PHONE_REGEX, phone_clean):
            errors.append("Invalid phone number")

    # Validate sex
    sex = record.get("sex")
    if sex:
        if str(sex).strip().lower() not in ["male", "female", "other"]:
            errors.append("Invalid sex value")

    return errors
