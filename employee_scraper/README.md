# Employee Data Scraper

Scrapes employee data from a Google Drive file and validates it before ingestion.

## Features
- File download with retry
- CSV & Excel support
- Schema validation
- Record-level validation
- Logging & unit tests

## ▶️ How to Run the Project
```bash
python -m scraper.main
pytest -v


---

## 🚀 How to Run (Terminal)

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
pytest -v

## Improvements
- Improved validation logic and test coverage
