from google_auth_oauthlib.flow import InstalledAppFlow
import os

# Scopes required for the AdMob API
SCOPES = ['https://www.googleapis.com/auth/admob.readonly']

def get_access_token():
    # Path to your OAuth 2.0 credentials JSON file
    creds_file = 'credentials.json'

    # Create the flow using the client secrets file and the scopes
    flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
    
    # Run the local server to authorize the user
    creds = flow.run_local_server(port=0)
    
    # Print the access token
    print(f'Access Token: {creds.token}')

    # Optionally, save credentials for future use
    with open('token.json', 'w') as token_file:
        token_file.write(f'{{"access_token": "{creds.token}", "refresh_token": "{creds.refresh_token}", "token_uri": "{creds.token_uri}", "client_id": "{creds.client_id}", "client_secret": "{creds.client_secret}"}}')

if __name__ == '__main__':
    get_access_token()
