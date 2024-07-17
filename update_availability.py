import os
import requests
import json
from jq import jq

# Set your API token here
PROXYCRAWL_API_KEY = 'jp70Vjnt8mVVP1Fq-DkXCw'
countries = ["US"]  # List of countries to check

# Function to check availability using ProxyCrawl API
def check_availability(video_url, country):
    url = f"https://api.proxycrawl.com/?token={PROXYCRAWL_API_KEY}&country_code={country}&url={video_url}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('status', 500) == 200
    else:
        print(f"Error: Failed to fetch availability for {video_url} in {country} - {url}")
        return False

# Read and parse channels.json
with open('channels.json', 'r') as f:
    channels = json.load(f)

for channel in channels['TV']:
    if 'Video' in channel:
        video_url = channel['Video']
        print(f"Checking availability for: {video_url}")
        available_countries = []

        for country in countries:
            if check_availability(video_url, country):
                available_countries.append(country)

        # Update the availability in the channel's JSON
        for ch in channels['TV']:
            if ch.get('Video') == video_url:
                ch['availability'] = {country: True for country in available_countries}

# Write the updated JSON back to the file
with open('channels.json', 'w') as f:
    json.dump(channels, f, indent=4)

# Commit and push changes
os.system('git config --global user.email "7keyzbeatz@gmail.com"')
os.system('git config --global user.name "7keyzbeatz"')
os.system('git add channels.json')
os.system('git commit -m "Update channel availability"')
os.system('git push')
