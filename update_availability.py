import json
import requests

# Set your API token here
PROXYCRAWL_API_KEY = '###NOTE###jp70Vjnt8mVVP1Fq-DkXCw###NOTE###'
countries = ["US"]  # List of countries to check

# Function to check availability of video URL
def check_availability(video_url):
    try:
        response = requests.head(video_url, allow_redirects=True)
        if response.status_code == 200:
            # Now check if the content is accessible
            final_url = response.url
            final_response = requests.get(final_url)
            if final_response.status_code == 200:
                return True
            else:
                print(f"Error: Final URL {final_url} returned status code {final_response.status_code}")
                return False
        elif response.status_code == 302:
            redirected_url = response.headers.get('Location')
            if redirected_url:
                print(f"Video URL redirected to: {redirected_url}")
                # Now recursively check availability of the redirected URL
                return check_availability(redirected_url)
            else:
                print(f"Error: Video URL {video_url} redirected but no Location header found")
                return False
        else:
            print(f"Error: Video URL {video_url} returned status code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch video URL {video_url} - {str(e)}")
        return False

# Load channels.json
try:
    with open('channels.json', 'r') as f:
        channels = json.load(f)
except FileNotFoundError:
    print("Error: channels.json file not found")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON from channels.json: {str(e)}")
    exit(1)

# Update availability for each channel in 'TV' list
for channel in channels['TV']:
    if 'Video' in channel:
        video_url = channel['Video']
        print(f"Checking availability for: {video_url}")
        available_countries = []

        # Check availability for each country
        for country in countries:
            if check_availability(video_url):
                available_countries.append(country)

        # Update availability in the channel's JSON
        channel['availability'] = {country: True for country in available_countries}

# Write the updated JSON back to the file
with open('channels.json', 'w') as f:
    json.dump(channels, f, indent=4)

print("Availability update completed.")
