import requests

# Replace with your actual values
CLIENT_ID = '824351498537-5gra4r14ngcgeti42a9hl1qjb2geti6j.apps.googleusercontent.com'
CLIENT_SECRET = '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'
AUTHORIZATION_CODE = '4/0AcvDMrCNZE1EGV8LBeUI1ucbjNv7J2feDtFSyqA8HHxtgt5cwA_Jc5O_L8POBhzKRMQnwA'
REDIRECT_URI = 'https://movieflixgrapp.vercel.app'

# URL to exchange the authorization code for an access token
TOKEN_URI = 'https://oauth2.googleapis.com/token'

# Parameters to send in the request
data = {
    'code': AUTHORIZATION_CODE,
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'redirect_uri': REDIRECT_URI,
    'grant_type': 'authorization_code'
}

# Make the request to get the access token
response = requests.post(TOKEN_URI, data=data)
token_data = response.json()

# Print the response for debugging
print("Response Code:", response.status_code)
print("Response Body:", token_data)

# Check if the response contains the access token
if 'access_token' in token_data:
    access_token = token_data['access_token']
    print(f"Access Token: {access_token}")
else:
    print(f"Error: {token_data.get('error_description', 'Unknown error')}")
