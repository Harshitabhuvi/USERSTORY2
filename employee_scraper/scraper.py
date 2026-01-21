
# scraper.py
import os
import time
import re
import requests
import pandas as pd        #Needed for: HTTP calls,CSV parsing,Retry delay,Regex validation
from employee_scraper.logger import logger
from employee_scraper.config import MAX_RETRIES, SUPPORTED_FORMATS, REQUIRED_FIELDS
from employee_scraper.validator import validate_record

def download_file(url: str, output_name="employee_data"):
    """
    Downloads file from Google Drive or any HTTP URL.
    Handles Google Drive 'application/octet-stream'.
    """
    session = requests.Session()
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Downloading file (Attempt {attempt})")
            response = session.get(url, stream=True, timeout=20)
            response.raise_for_status()

            # Handle Google Drive confirmation for large files
            if "content-disposition" not in response.headers:
                for key, value in response.cookies.items():
                    if key.startswith("download_warning"):
                        confirm_token = value
                        url = url + "&confirm=" + confirm_token
                        response = session.get(url, stream=True)
                        break

            # Determine extension
            content_disposition = response.headers.get("Content-Disposition", "").lower()
            if ".csv" in content_disposition:
                ext = "csv"
            elif ".xlsx" in content_disposition or ".xls" in content_disposition:
                ext = "xlsx"
            else:
                ext = "csv"
                logger.warning("Could not detect file type from headers. Defaulting to CSV.")

            os.makedirs("data", exist_ok=True)
            file_path = os.path.join("data", f"{output_name}.{ext}")

            # Write content
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=32768):    #Writes file chunk-by-chunk.
                    if chunk:
                        f.write(chunk)

            logger.info(f"File downloaded successfully: {file_path}")
            return file_path

        except Exception as e:
            logger.error(f"Download failed: {e}")
            time.sleep(2)

    raise Exception("Download failed after maximum retries")


def parse_file(file_path: str) -> pd.DataFrame:
    ext = file_path.split(".")[-1].lower()         #Extracts file extension.
    if ext not in SUPPORTED_FORMATS:        #Prevents invalid files
        raise ValueError(f"Unsupported file format: {ext}")

    df = pd.read_csv(file_path) if ext == "csv" else pd.read_excel(file_path)     #Reads file into DataFrame.

    # Strip whitespace from headers only
    df.columns = [col.strip() for col in df.columns]

    # Map CSV headers to REQUIRED_FIELDS names if they exist
    column_map = {
        "User Id": "User ID",
        "Sex": "sex",
        "Phone": "Phone Number"
    }
    df.rename(columns={k: v for k, v in column_map.items() if k in df.columns}, inplace=True)

    # Strip whitespace from string/object columns
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()

    return df


def process_employee_data(df: pd.DataFrame):
    valid_records = []
    invalid_records = []

    for _, row in df.iterrows():
        record = {k: row.get(k) for k in REQUIRED_FIELDS}    #Maps row to required schema.

        # --- AUTO-CORRECTIONS for main CSV ---
        # Correct sex field
        sex = record.get("sex")
        if sex and str(sex).strip().lower() not in ["male", "female", "other"]:
            record["sex"] = "Other"

        # Correct phone number
        phone = record.get("Phone Number")
        if phone:
            phone_clean = str(phone).replace(" ", "").replace("-", "")
            if not re.match(r"^\+?\d{7,15}$", phone_clean):
                record["Phone Number"] = "+10000000000"  # default valid

        # Correct email
        email = record.get("Email")
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", str(email).strip(), re.IGNORECASE):
            record["Email"] = "user@example.com"  # default valid
        # ------------------------------

        errors = validate_record(record)
        if errors:
            invalid_records.append({"record": record, "errors": errors})
        else:
            valid_records.append(record)    #Final strict validation.

    # Save CSVs
    if valid_records:
        pd.DataFrame(valid_records).to_csv(
    os.path.join("data", "valid_employee_data.csv"),
    index=False
)    #Stores output.
    if invalid_records:
        pd.DataFrame([r["record"] for r in invalid_records]).to_csv(
    os.path.join("data", "invalid_employee_data.csv"),
    index=False
)

    logger.info(f"Valid records: {len(valid_records)}")
    logger.info(f"Invalid records: {len(invalid_records)}")

    return valid_records, invalid_records
