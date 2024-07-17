import json
import os
import requests

# Set your API token here
PROXYCRAWL_API_KEY = 'jp70Vjnt8mVVP1Fq-DkXCw'
countries = ["US"]  # List of countries to check

# Function to check availability using ProxyCrawl API
def check_availability(video_url, country):
    url = f"https://api.proxycrawl.com/?token={PROXYCRAWL_API_KEY}&country_code={country}&url={video_url}&format=html"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            print(f"Error: Failed to fetch availability for {video_url} in {country} - Status Code: {response.status_code}")
            return False
    
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch availability for {video_url} in {country} - {str(e)}")
        return False

# Example usage with channels.json
try:
    with open('channels.json', 'r') as f:
        channels = json.load(f)
except FileNotFoundError:
    print("Error: channels.json file not found")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON from channels.json: {str(e)}")
    exit(1)

for channel in channels['TV']:
    if 'Video' in channel:
        video_url = channel['Video']
        print(f"Checking availability for: {video_url}")
        available_countries = []

        for country in countries:
            if check_availability(video_url, country):
                available_countries.append(country)

        # Update the availability in the channel's JSON
        channel['availability'] = {country: True for country in available_countries}

# Write the updated JSON back to the file
with open('channels.json', 'w') as f:
    json.dump(channels, f, indent=4)

# Commit and push changes
os.system('git config --global user.email "7keyzbeatz@gmail.com"')
os.system('git config --global user.name "7keyzbeatz"')
os.system('git add channels.json')
os.system('git commit -m "Update channel availability"')
os.system('git push')
