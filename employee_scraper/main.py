from employee_scraper.scraper import download_file, parse_file, process_employee_data
from employee_scraper.config import GOOGLE_DRIVE_URL
from employee_scraper.validator import validate_record


# Enable relaxed validation for main CSV run
TEST_MODE = True


# def main():
#     url = "https://drive.google.com/uc?id=1AWPf-pJodJKeHsARQK_RHiNsE8fjPCVK&export=download"
#     file_path = download_file(url)            #Downloads file.
#     df = parse_file(file_path)              #Parses into DataFrame.
#     df.to_csv("data/employee_data.csv", index=False)
#     process_employee_data(df)              #Validates & stores records.
def main():
    url = "https://drive.google.com/uc?id=1AWPf-pJodJKeHsARQK_RHiNsE8fjPCVK&export=download"
    file_path = download_file(url)
    df = parse_file(file_path)
    process_employee_data(df)

if __name__ == "__main__":                #Ensures script runs only when executed directly.
    main()
