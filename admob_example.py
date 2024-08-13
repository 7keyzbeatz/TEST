from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
import os
import json

def main():
    try:
        # Load the access token from the file or environment
        with open('token.json') as token_file:
            token_data = json.load(token_file)
            creds = Credentials(
                token_data['access_token'],
                refresh_token=token_data['refresh_token'],
                token_uri=token_data['token_uri'],
                client_id=token_data['client_id'],
                client_secret=token_data['client_secret']
            )

        # Initialize the AdMob API service
        service = build('admob', 'v1', credentials=creds)

        # Example API call - replace with actual call as needed
        response = service.accounts().list().execute()
        
        # Print response or process as needed
        print(response)
    
    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
