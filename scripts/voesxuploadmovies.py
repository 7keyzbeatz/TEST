import requests
import json
import time

# Function to upload to voe.sx and get file_code
def upload_to_voe(api_key, video_url, folder_id):
    api_url = f'https://voe.sx/api/upload/url?key={api_key}&url={video_url}&folder_id={folder_id}'
    print(f"Uploading URL: {video_url} to voe.sx...")

    response = requests.post(api_url)
    if response.status_code == 200 and response.json().get('success'):
        file_code = response.json()['result']['file_code']
        print(f"Upload successful! File code: {file_code}")
        return file_code
    else:
        print(f"Failed to upload: {response.status_code}, {response.text}")
        return None

# Function to check ongoing uploads
def check_uploads(api_key):
    api_url = f'https://voe.sx/api/upload/url/list?key={api_key}'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        ongoing_uploads = [upload for upload in data['list']['data'] if upload['status'] < 3]  # Assuming status < 3 indicates ongoing
        return ongoing_uploads
    else:
        print(f"Failed to fetch upload list: {response.status_code}, {response.text}")
        return []

# Function to process movies in batches
def process_movies_in_batches(movies, batch_size, api_key, folder_id):
    total_movies = len(movies)
    i = 0

    while i < total_movies:
        # Wait until there are no ongoing uploads
        print(f"\nChecking ongoing uploads...")
        while len(check_uploads(api_key)) > 0:
            print(f"Ongoing uploads detected. Waiting before retrying...")
            time.sleep(30)  # Wait 30 seconds before checking again

        # Process the next batch of movies
        batch = movies[i:i + batch_size]
        print(f"\nProcessing batch {i // batch_size + 1} of {total_movies // batch_size + 1}...")

        for movie in batch:
            movie_id = movie.get("TMDB_ID", "Unknown")
            movie_title = movie.get("Title", "Unknown Title")
            direct_video_url = movie.get("DirectVideo")

            if direct_video_url:
                print(f"\nProcessing movie ID: {movie_id}, Title: {movie_title}")
                file_code = upload_to_voe(api_key, direct_video_url, folder_id)
                if file_code:
                    movie["VOE_ID"] = file_code
                    print(f"Added VOE_ID {file_code} to movie {movie['Title']}")
                else:
                    print(f"Could not add VOE_ID to movie {movie['Title']}")
                time.sleep(1)  # To avoid hitting rate limits

        i += batch_size  # Move to the next batch

        # Wait for current batch uploads to complete
        print(f"Waiting for uploads to complete before processing the next batch...")
        while len(check_uploads(api_key)) > 0:
            print(f"Uploads still ongoing. Checking again in 30 seconds...")
            time.sleep(30)  # Wait 30 seconds before checking again

        # Optionally pause between batches
        print(f"Waiting before processing the next batch...")
        time.sleep(10)  # Adjust as needed

    print("All movies processed.")

# Load movies JSON from the local repository
with open('movies.json', 'r') as f:
    movies_json = json.load(f)

# Your API key and folder ID
api_key = 'vU09m2ekakGBqEw9ewfxAwxyiUtlClAKEhIbMavmmvI6Ob9vawParVv7cZ0Id6YI'  # Replace with your actual API key
folder_id = 50460  # Replace with the actual folder ID
batch_size = 25  # Process 25 movies at a time

if movies_json:
    # Process movies in batches
    process_movies_in_batches(movies_json.get("Movies", []), batch_size, api_key, folder_id)

    # Save the updated JSON to a local file
    with open('updated_movies.json', 'w') as f:
        json.dump(movies_json, f, indent=4)

    print("Updated movies JSON saved to 'updated_movies.json'")
else:
    print("No data found in movies.json.")
