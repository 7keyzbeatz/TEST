import requests
import json

# Your client credentials
CLIENT_ID = '824351498537-5gra4r14ngcgeti42a9hl1qjb2geti6j.apps.googleusercontent.com'
CLIENT_SECRET = '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'
REFRESH_TOKEN = '1//09YOifK_foTerCgYIARAAGAkSNwF-L9IrRISLb6ERCdcR5GOED6LyTH19YEoM2cHlSyqExP-Bnp6xD8xU7n_4hRoDO5veLAEi4c8'

# Your Publisher ID
PUBLISHER_ID = 'pub-1669215305824306'

# Step 1: Use the refresh token to get a new access token
def get_access_token():
    token_url = 'https://oauth2.googleapis.com/token'
    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': REFRESH_TOKEN,
        'grant_type': 'refresh_token'
    }
    response = requests.post(token_url, data=params)
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token
    else:
        raise Exception(f"Failed to refresh token: {response.text}")

# Step 2: Use the access token to make a POST request to the AdMob API
def generate_network_report(access_token):
    api_url = f'https://admob.googleapis.com/v1/accounts/{PUBLISHER_ID}/networkReport:generate'
    
    # Adjust the request body based on the correct format
    request_body = {
        "reportSpec": {
            "dateRange": {
                "startDate": {
                    "year": 2024,
                    "month": 1,
                    "day": 1
                },
                "endDate": {
                    "year": 2024,
                    "month": 8,
                    "day": 14
                }
            },
            "dimensions": ["DATE"],
            "metrics": ["MATCH_RATE"],
            "timeZone": []  # Note: Adjust based on whether you need a specific time zone or not
        }
    }
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(api_url, headers=headers, data=json.dumps(request_body))
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to generate network report: {response.text}")

# Example usage:
if __name__ == "__main__":
    try:
        access_token = get_access_token()
        report_data = generate_network_report(access_token)
        print(json.dumps(report_data, indent=2))
    except Exception as e:
        print(e)
