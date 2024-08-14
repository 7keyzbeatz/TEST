import os
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from datetime import datetime, timedelta

def get_access_token(client_id, client_secret, refresh_token):
    token_url = 'https://oauth2.googleapis.com/token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    response = requests.post(token_url, data=params)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()['access_token']

def fetch_admob_data(credentials, publisher_id):
    service = build('admob', 'v1', credentials=credentials)

    # Define time range for today's data
    now = datetime.utcnow()
    start_date = now.strftime('%Y-%m-%d')
    end_date = (now + timedelta(days=1)).strftime('%Y-%m-%d')

    # Create API request
    request = {
        'report_spec': {
            'date_range': {
                'start_date': start_date,
                'end_date': end_date
            },
            'dimensions': ['DATE'],
            'metrics': ['ESTIMATED_EARNINGS'],  # Example metric, replace as needed
            'time_zone': 'UTC'
        }
    }

    response = service.accounts().networkReport().generate(parent=f'accounts/{publisher_id}', body=request).execute()
    
    # Process and print the response
    earnings = response['rows'][0]['metrics'][0]['value']
    print(f"Today's estimated earnings: {earnings}")

def main():
    # Environment variables set via GitHub Actions secrets
    client_id = os.getenv('OAUTH_CLIENT_ID')
    client_secret = os.getenv('OAUTH_CLIENT_SECRET')
    refresh_token = os.getenv('OAUTH_REFRESH_TOKEN')
    publisher_id = 'pub-1669215305824306'  # Replace with your actual AdMob publisher ID

    # Get access token using the refresh token
    access_token = get_access_token(client_id, client_secret, refresh_token)

    # Set up credentials
    credentials = Credentials(token=access_token)

    # Fetch and process AdMob data
    fetch_admob_data(credentials, publisher_id)

if __name__ == "__main__":
    main()
