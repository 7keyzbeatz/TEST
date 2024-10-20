import json
import os
import time
import requests
from requests.exceptions import ConnectionError, Timeout

# Configuration details
CONFIG = {
    'voe': {
        'api_key': 'vU09m2ekakGBqEw9ewfxAwxyiUtlClAKEhIbMavmmvI6Ob9vawParVv7cZ0Id6YI'  # Replace with your Voe API key
    },
    'upload': {
        'endpoint': 'https://voe.sx/api/upload/url',
        'parameters': {
            'folder': '50460'  # Replace with your folder ID
        }
    },
    'json_file': {
        'path': 'data/movies.json'  # Replace with your JSON file path
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

# Upload video to Voe
def upload_to_voe(api_key, direct_video_url, folder_id, retries=3, delay=5):
    api_url = f"https://voe.sx/api/upload/url?key={api_key}&url={direct_video_url}&folder_id={folder_id}"
    
    for attempt in range(retries):
        try:
            # Adding a timeout of 30 seconds
            response = requests.post(api_url, timeout=30)
            response.raise_for_status()  # Raise HTTPError for bad responses
            
            # Check if the response is successful
            if response.status_code == 200:
                result = response.json()
                if result['status'] == 200:
                    file_code = result['result']['file_code']
                    print(f"Successfully uploaded. File code: {file_code}")
                    return file_code
                else:
                    print(f"Error: {result['msg']}")
                    return None
            else:
                print(f"Error: Failed with status code {response.status_code}")
                return None

        except (ConnectionError, Timeout) as e:
            print(f"Connection error or timeout occurred: {e}")
            if attempt < retries - 1:
                print(f"Retrying... (Attempt {attempt + 1}/{retries})")
                time.sleep(delay)
            else:
                print("Max retries exceeded. Exiting.")
                return None

# Process movies in batches
def process_movies_in_batches(movies, start_index, end_index, batch_size, api_key, folder_id):
    for i in range(start_index, end_index, batch_size):
        batch = movies[i:i + batch_size]
        print(f"Processing batch {i // batch_size + 1} of {len(movies) // batch_size + 1}...")
        
        for movie in batch:
            # Safely get the 'ID' and 'Title' keys with default values
            movie_id = movie.get('ID', 'Unknown ID')  # Use 'Unknown ID' if the key is missing
            title = movie.get('Title', 'Untitled')    # Use 'Untitled' if the key is missing
            direct_video_url = movie['DirectVideo']   # Assuming 'DirectVideo' always exists
            
            print(f"Processing movie ID: {movie_id}, Title: {title}")
            file_code = upload_to_voe(api_key, direct_video_url, folder_id)
            
            if file_code:
                movie['FileCode'] = file_code
            else:
                print(f"Failed to upload movie: {title}")
        
        # Optional: Sleep for a few seconds between batches to avoid overwhelming the server
        time.sleep(5)
        
def main():
    # Extract configuration details
    api_key = CONFIG['voe']['api_key']
    folder_id = CONFIG['upload']['parameters']['folder']
    json_file_path = CONFIG['json_file']['path']
    
    # Load movie data
    data = load_json(json_file_path)
    
    # Define the batch processing parameters
    start_index = 0
    end_index = len(data['Movies'])
    batch_size = 10  # Adjust the batch size as needed
    
    # Process the movies in batches
    process_movies_in_batches(data['Movies'], start_index, end_index, batch_size, api_key, folder_id)
    
    # Save updated movie data with Streamtape file codes
    save_json(json_file_path, data)

if __name__ == "__main__":
    main()
