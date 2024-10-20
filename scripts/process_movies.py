import json
import requests

# Function to load JSON data from a file
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to save updated JSON data to a file
def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Function to upload videos to voe.sx
def upload_to_voe(api_key, direct_video_url, folder_id):
    # Construct the API URL for voe.sx
    api_url = f"https://voe.sx/api/upload/url?key={api_key}&url={direct_video_url}&folder_id={folder_id}"

    try:
        # Send POST request to voe.sx API
        response = requests.post(api_url)
        response.raise_for_status()  # Raise an error for any HTTP status codes >= 400

        # Parse the response JSON
        result = response.json()

        # Check if the HTTP status code is 200 and API status is 'ok'
        if response.status_code == 200 and result.get('status') == "ok":
            file_code = result.get('filecode')
            print(f"Successfully uploaded. File code: {file_code}")
            return file_code
        elif result.get('msg') == "already in queue":
            print(f"Video URL '{direct_video_url}' is already in the upload queue.")
            return "already_in_queue"
        else:
            print(f"Upload failed. Response: {result}")
            return None
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error occurred: {errh}")
        return None
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
        return None
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return None

# Function to process movies in batches and upload them to voe.sx
def process_movies_in_batches(movies, start_index, end_index, batch_size, api_key, folder_id):
    for i in range(start_index, min(end_index, len(movies))):
        movie = movies[i]
        direct_video_url = movie.get('DirectVideo')
        title = movie.get('Title', 'Unknown Title')
        
        # Debug: Print the entire movie data to identify structure
        print(f"Processing movie {i+1}/{len(movies)}: {title}")
        print(f"Movie details: {movie}")

        # Try to access the movie ID and print it for debugging
        movie_id = movie.get('ID')  # Use the correct key for movie ID

        # Debug: Log if the ID is found
        if movie_id:
            print(f"Movie ID: {movie_id}")
        else:
            print(f"Warning: No ID found for '{title}'.")

        if not movie_id:
            continue

        # Try to upload to voe.sx
        file_code = upload_to_voe(api_key, direct_video_url, folder_id)

        # Skip if already in queue
        if file_code == "already_in_queue":
            print(f"Skipping '{title}', as it is already in the upload queue.")
            continue

        if file_code:
            movie['FileCode'] = file_code
        else:
            print(f"Failed to upload '{title}'")

# Main function to load the movie data, process in batches, and save the updated data
def main():
    # Configuration details
    config = {
        'api_key': 'vU09m2ekakGBqEw9ewfxAwxyiUtlClAKEhIbMavmmvI6Ob9vawParVv7cZ0Id6YI',  # Replace with your voe.sx API key
        'folder_id': '50460',  # Folder ID to upload the videos into
        'json_file_path': 'data/movies.json',  # Path to the JSON file containing movie data
        'batch_size': 25  # Number of movies to process per batch
    }

    # Load the JSON data from file
    data = load_json(config['json_file_path'])
    
    # Define the batch processing range
    start_index = 0
    end_index = 30

    # Process the movies in batches
    process_movies_in_batches(data['Movies'], start_index, end_index, config['batch_size'], config['api_key'], config['folder_id'])

    # Save the updated data back to the JSON file
    save_json(config['json_file_path'], data)

if __name__ == "__main__":
    main()
