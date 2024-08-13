from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

def main():
    # Replace with the path to your service account JSON file
    SERVICE_ACCOUNT_FILE = 'service_account_key.json'
    SCOPES = ['https://www.googleapis.com/auth/admob.readonly']

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    service = build('admob', 'v1', credentials=credentials)

    # Example API call
    response = service.accounts().mediationReport().generate(
        parent='accounts/YOUR_ACCOUNT_ID',
        body={
            "reportSpec": {
                "dateRange": {
                    "startDate": "2024-08-01",
                    "endDate": "2024-08-01"
                },
                "metrics": ["MATCH_RATE"]
            }
        }
    ).execute()

    # Print the results for GitHub Actions logs
    print(json.dumps(response, indent=2))

if __name__ == '__main__':
    main()
