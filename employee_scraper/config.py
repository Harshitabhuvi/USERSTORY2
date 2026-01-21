GOOGLE_DRIVE_URL = (
    "https://drive.google.com/uc?id=1AWPf-pJodJKeHsARQK_RHiNsE8fjPCVK&export=download"
)

MAX_RETRIES = 3         #Limits retry attempts.Prevents infinite loops.
SUPPORTED_FORMATS = ["csv", "xlsx"]

REQUIRED_FIELDS = [          #equired employee schema.Used everywhere (validation, parsing).
    "User ID",
    "First Name",
    "Last Name",
    "sex",
    "Email",
    "Job Title",
    "Phone Number",
]
