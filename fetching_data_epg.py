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
    try:
        response = requests.get("https://worldtimeapi.org/api/timezone/Europe/Athens")
        if response.status_code == 200:
            current_time = datetime.fromisoformat(response.json()["datetime"].replace("Z", "+00:00")).timestamp() * 1000
            return int(current_time)
        else:
            raise Exception(f"Failed to fetch current time. Status code: {response.status_code}")
    except Exception as e:
        raise Exception(f"Failed to fetch current time: {str(e)}")

def update_basic_version_tv(data):
    with open("basicVersionTV.json", "w") as f:
        json.dump(data, f, indent=4)

def main():
    github_api = GitHubAPI()
    
    try:
        # Read basicVersionTV.json file
        print("Reading basicVersionTV.json file...")
        basic_version_tv_data = read_basic_version_tv()
        print(f"basicVersionTV.json data: {basic_version_tv_data}")
        
        # Fetch overview.json content from the specified Gist
        gist_id = "4cd6b3c4ede5f5433b7f4c54a86459e5"
        gist_filename = "overview.json"
        print(f"Fetching content from Gist: {gist_id}, file: {gist_filename}...")
        gist_content = github_api.get_gist_content(gist_id, gist_filename)
        print(f"Received gist content: {gist_content}")
        
        # Fetch current time in milliseconds
        print("Fetching current time in milliseconds...")
        current_time_ms = fetch_current_time_ms()
        print(f"Current time in milliseconds: {current_time_ms}")
        
        # Update basicVersionTV.json with fetched program information
        for channel_name, channel_items in basic_version_tv_data.items():
            for item in channel_items:
                if "SKey" in item:
                    for channel in gist_content:
                        if channel.get("n") == item["SKey"] and "schedules" in channel:
                            for schedule in channel["schedules"]:
                                start_time = schedule.get("s")
                                end_time = schedule.get("e")
                                title = schedule.get("t")
                                description = schedule.get("d")
                                
                                if start_time is not None and end_time is not None:
                                    if start_time <= current_time_ms <= end_time:
                                        item["t"] = title
                                        item["d"] = description
                                        item["s"] = start_time
                                        item["e"] = end_time
                                        print(f"Updated values for {item['SKey']}:")
                                        print(f"t: {item['t']}")
                                        print(f"d: {item['d']}")
                                        print(f"s: {item['s']}")
                                        print(f"e: {item['e']}\n")
        
        # Write updated basicVersionTV.json back to file
        update_basic_version_tv(basic_version_tv_data)
        print("basicVersionTV.json updated successfully.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
