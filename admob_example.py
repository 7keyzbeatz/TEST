import sys
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def main():
    # Get the service account JSON from the command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python admob_example.py <service_account_json>")
        sys.exit(1)

    service_account_json = sys.argv[1]

    try:
        # Load the JSON string into a dictionary
        service_account_info = json.loads(service_account_json)
        
        # Set up credentials and service
        SCOPES = ['https://www.googleapis.com/auth/admob.readonly']
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info, scopes=SCOPES
        )

        service = build('admob', 'v1', credentials=credentials)

        # Example API call
        response = service.accounts().mediationReport().generate(
            parent='accounts/pub-1669215305824306',
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
