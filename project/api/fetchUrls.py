import requests
import json
import re

# Function to get the URL for a given channel name
def main_function():
    # Example list of Twitch URLs (can be dynamically passed as input)
    channels = [
        "https://www.twitch.tv/livethess03",
        "https://www.twitch.tv/someOtherChannel"
    ]
    
    # Generate the request URLs for each channel
    results = []
    for channel in channels:
        result = fetch_m3u8_url(channel)
        results.append(result)
    
    return json.dumps({
        "Type": "HTTPRequestNeeded",
        "Results": results  # Multiple results
    })

# Function to handle the HTTP request and fetch .m3u8 URL
def fetch_m3u8_url(channel_url):
    try:
        # Construct the API URL dynamically with the provided channel URL
        api_url = f"https://pwn.sh/tools/streamapi.py?url={channel_url}"
        response = requests.get(api_url)

        if response.status_code != 200:
            return {
                "Type": "Error",
                "Result": f"Failed to fetch data for {channel_url}",
                "enabledDRM": False,
                "requiredHeaders": False
            }
        
        # Process the response to extract the .m3u8 URL
        response_string = response.text
        m3u8_url = extract_url(response_string, ".m3u8")

        if m3u8_url:
            return {
                "Type": "Direct",
                "Result": m3u8_url,
                "enabledDRM": False,
                "requiredHeaders": False
            }
        else:
            return {
                "Type": "Error",
                "Result": "No .m3u8 URL found",
                "enabledDRM": False,
                "requiredHeaders": False
            }

    except Exception as e:
        return {
            "Type": "Error",
            "Result": f"Error processing {channel_url}: {str(e)}",
            "enabledDRM": False,
            "requiredHeaders": False
        }

# Helper function to extract a URL based on a keyword (e.g., .m3u8)
def extract_url(input_string, keyword):
    # Search for the keyword in the string
    matches = re.findall(r'".*?' + re.escape(keyword) + r'.*?"', input_string)
    if matches:
        # Return the first match (the .m3u8 URL)
        return matches[0].strip('"')
    else:
        return None

# Example usage (you can trigger this from a server or request handler)
if __name__ == "__main__":
    # Get the combined response with multiple m3u8 URLs
    response = main_function()
    print(response)
