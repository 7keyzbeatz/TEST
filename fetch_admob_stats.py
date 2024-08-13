import os
import requests

# Constants
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
AUTHORIZATION_CODE = os.getenv('AUTHORIZATION_CODE')
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
TOKEN_URI = 'https://oauth2.googleapis.com/token'
ADMOB_API_URL = 'https://admob.googleapis.com/v1/accounts'  # Adjust endpoint as needed for fetching stats

def get_access_token():
    """Obtain OAuth 2.0 access token using the authorization code."""
    data = {
        'code': AUTHORIZATION_CODE,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    
    response = requests.post(TOKEN_URI, data=data)
    
    if response.status_code != 200:
        print(f"Error obtaining access token: {response.status_code}")
        print(response.text)
        return None

    token_data = response.json()
    access_token = token_data.get('access_token')
    
    if access_token:
        print(f"Access Token: {access_token}")
        return access_token
    else:
        print("Error: No access token found")
        return None

def fetch_admob_stats(access_token):
    """Fetch AdMob statistics using the access token."""
    # Example endpoint to get AdMob account details, adjust as needed
    url = f"{ADMOB_API_URL}/YOUR_ACCOUNT_ID/stats"  # Replace with your AdMob account ID and appropriate endpoint
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching AdMob stats: {response.status_code}")
        print(response.text)
        return None

    stats_data = response.json()
    
    # Print or process the stats data
    print("AdMob Stats:")
    print(stats_data)

def main():
    access_token = get_access_token()
    if access_token:
        fetch_admob_stats(access_token)

if __name__ == '__main__':
    main()
