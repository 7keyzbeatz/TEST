import sys
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def main():
    if len(sys.argv) != 2:
        print("Usage: python admob_example.py <service_account_json_file>")
        sys.exit(1)

    json_file_path = sys.argv[1]

    try:
        # Read the JSON from the file
        with open(json_file_path, 'r') as json_file:
            service_account_info = json.load(json_file)
        
        # Set up credentials and service
        SCOPES = ['https://www.googleapis.com/auth/admob.readonly']
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info, scopes=SCOPES
        )

        service = build('admob', 'v1', credentials=credentials)

        # Replace 'YOUR_ACCOUNT_ID' with your actual AdMob Account ID
        response = service.accounts().mediationReport().generate(
            parent='accounts/YOUR_ACCOUNT_ID',  # <-- Replace with your actual AdMob Account ID
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

    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
