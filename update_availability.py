import os
import json
import requests
from bs4 import BeautifulSoup

# Set your API token here
PROXYCRAWL_API_KEY = 'jp70Vjnt8mVVP1Fq-DkXCw'
countries = ["US"]  # List of countries to check

# Function to check availability using ProxyCrawl API
def check_availability(video_url, country):
    url = f"https://api.proxycrawl.com/?token={PROXYCRAWL_API_KEY}&country_code={country}&url={video_url}&format=html"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx and 5xx)
        
        # Check if response is HTML content
        if response.headers.get('Content-Type', '').lower().startswith('text/html'):
            soup = BeautifulSoup(response.content, 'html.parser')
            # Example: Check if certain element exists indicating availability
            if soup.find('div', {'class': 'availability'}):
                return True
            else:
                return False
        else:
            print(f"Error: Expected HTML content for {video_url} in {country}, got {response.headers.get('Content-Type', '')}")
            return False
    
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch availability for {video_url} in {country} - {url}")
        print(f"Exception: {e}")
        return False

# Example usage with channels.json
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
