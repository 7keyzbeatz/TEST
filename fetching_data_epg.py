import json
import requests
from datetime import datetime

class GitHubAPI:
    def __init__(self):
        self.base_url = "https://api.github.com"

    def get_gist_content(self, gist_id, filename):
        url = f"{self.base_url}/gists/{gist_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            gist_data = response.json()
            if filename in gist_data["files"]:
                raw_url = gist_data["files"][filename]["raw_url"]
                response = requests.get(raw_url)
                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception(f"Failed to fetch content from Gist file {filename}. Status code: {response.status_code}")
            else:
                raise Exception(f"File {filename} not found in Gist.")
        else:
            raise Exception(f"Failed to fetch Gist {gist_id}. Status code: {response.status_code}")

def read_basic_version_tv():
    with open("basicVersionTV.json", "r") as f:
        data = json.load(f)
    return data

def fetch_current_time_ms():
    # Using an example API to fetch current time in milliseconds
    response = requests.get("http://worldclockapi.com/api/json/utc/now")
    if response.status_code == 200:
        current_time = response.json()["currentFileTime"]
        return int(current_time)
    else:
        raise Exception(f"Failed to fetch current time. Status code: {response.status_code}")

def main():
    # Initialize GitHub API client
    github_api = GitHubAPI()
    
    try:
        # Read basicVersionTV.json file
        basic_version_tv_data = read_basic_version_tv()
        
        # Extract SKey values from basicVersionTV.json
        skeys = [item["SKey"] for channel in basic_version_tv_data.values() for item in channel]
        
        # Fetch overview.json content from the specified Gist
        gist_id = "4cd6b3c4ede5f5433b7f4c54a86459e5"
        gist_filename = "overview.json"
        gist_content = github_api.get_gist_content(gist_id, gist_filename)
        
        # Fetch current time in milliseconds
        current_time_ms = fetch_current_time_ms()
        
        # Process each channel found in overview.json
        for channel in gist_content:
            if channel.get("n") in skeys:
                # Check if the current time falls within the schedule of the channel
                for schedule in channel.get("s", []):
                    start_time = schedule["s"]
                    end_time = schedule["e"]
                    title = schedule["t"]
                    description = schedule["d"]
                    
                    # Check if current_time_ms is between start_time and end_time
                    if start_time <= current_time_ms <= end_time:
                        print(f"Channel: {channel['n']}")
                        print(f"Playing Now: {title}")
                        print(f"Description: {description}\n")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
