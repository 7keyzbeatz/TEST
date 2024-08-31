import json
import os
import requests

# Configuration details
CONFIG = {
    'streamtape': {
        'login': '5477f76b8db471f43ff1',  # Replace with your Streamtape login
        'key': 'GQyP71q147slo3'       # Replace with your Streamtape key
    },
    'upload': {
        'endpoint': 'https://api.streamtape.com/remotedl/add',
        'parameters': {
            'folder': 'DR4b0ZpZJN4',  # Specify folder ID if needed
            'name_suffix': '.mp4'  # File name suffix
        }
    },
    'json_file': {
        'path': 'data/movies.json'
    }
}

# Load JSON data
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Save updated JSON data
def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Upload video to Streamtape
def upload_to_streamtape(video_url, title, streamtape_login, streamtape_key, upload_endpoint, folder, name_suffix):
    # Construct the request URL
    request_url = f"{upload_endpoint}?login={streamtape_login}&key={streamtape_key}&url={video_url}&folder={folder}&name={title}{name_suffix}"
    
    # Send GET request to the upload endpoint
    response = requests.get(request_url)
    
    if response.status_code == 200:
        result = response.json()
        if result['status'] == 200:
            streamtape_id = result['result']['id']
            print(f"Successfully added '{title}' to Streamtape with ID: {streamtape_id}")
            return streamtape_id
        else:
            print(f"Failed to add '{title}' to Streamtape. Error message: {result['msg']}")
            return None
    else:
        print(f"Failed to add '{title}' to Streamtape. Status code: {response.status_code}")
        return None

def main():
    # Extract configuration details
    streamtape_login = CONFIG['streamtape']['login']
    streamtape_key = CONFIG['streamtape']['key']
    upload_endpoint = CONFIG['upload']['endpoint']
    folder = CONFIG['upload']['parameters']['folder']
    name_suffix = CONFIG['upload']['parameters']['name_suffix']
    json_file_path = CONFIG['json_file']['path']
    
    # Load movie data
    data = load_json(json_file_path)
    
    # Process each movie
    for movie in data['Movies']:
        video_url = movie['DirectVideo']
        title = movie['Title']
        streamtape_id = upload_to_streamtape(video_url, title, streamtape_login, streamtape_key, upload_endpoint, folder, name_suffix)
        
        # Update movie entry with Streamtape ID if upload was successful
        if streamtape_id:
            movie['StreamtapeID'] = streamtape_id
    
    # Save updated movie data
    save_json(json_file_path, data)

if __name__ == "__main__":
    main()
