import requests

# Your client credentials
CLIENT_ID = '824351498537-5gra4r14ngcgeti42a9hl1qjb2geti6j.apps.googleusercontent.com'
CLIENT_SECRET = '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'
REFRESH_TOKEN = '1//09YOifK_foTerCgYIARAAGAkSNwF-L9IrRISLb6ERCdcR5GOED6LyTH19YEoM2cHlSyqExP-Bnp6xD8xU7n_4hRoDO5veLAEi4c8'

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
        raise Exception("Failed to refresh token: {}".format(response.text))

# Step 2: Use the access token to make a request to the AdMob API
def get_admob_data(access_token):
    api_url = 'https://admob.googleapis.com/v1/accounts/pub-1669215305824306'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch AdMob data: {}".format(response.text))

# Example usage:
if __name__ == "__main__":
    try:
        access_token = get_access_token()
        admob_data = get_admob_data(access_token)
        print(admob_data)
    except Exception as e:
        print(e)
