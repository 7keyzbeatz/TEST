import json
import requests
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load your API key
TMDB_API_KEY = '753fba9d8bfbd1068ebd0b4437209a8a'

# Function to fetch movie details from TMDB
def get_movie_details(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        genres = ", ".join([genre['name'] for genre in data.get('genres', [])])
        return {
            'runtime': data.get('runtime'),
            'genres': genres,
            'year': data.get('release_date', '').split('-')[0] if 'release_date' in data else None
        }
    else:
        logging.error(f"Failed to fetch details for TMDB_ID {tmdb_id}. Status Code: {response.status_code}")
        return {}

# Load the JSON file from the repository
json_file_path = 'data/movies_tmdb.json'
logging.info(f"Loading JSON data from {json_file_path}")
with open(json_file_path, 'r') as file:
    movies_data = json.load(file)

# Check if movies_data is loaded properly
if not movies_data or 'Movies' not in movies_data:
    logging.error("The JSON file doesn't contain the 'Movies' key or is empty.")
else:
    logging.info("JSON data loaded successfully.")

# Enrich the movies data with additional TMDB info
for movie in movies_data.get('Movies', []):
    if 'TMDB_ID' in movie:
        logging.info(f"Fetching details for movie: {movie.get('Title')} (TMDB_ID: {movie['TMDB_ID']})")
        details = get_movie_details(movie['TMDB_ID'])
        if details:
            movie.update(details)
            logging.info(f"Updated movie: {movie.get('Title')} with runtime: {details.get('runtime')}, genres: {details.get('genres')}, year: {details.get('year')}")
        else:
            logging.error(f"Failed to update movie: {movie.get('Title')}")
    else:
        logging.warning(f"Movie '{movie.get('Title')}' does not have a TMDB_ID.")

# Save the enriched data back to the same JSON file
output_file_path = json_file_path  # Save back to the same file
logging.info(f"Saving enriched JSON data to {output_file_path}")
with open(output_file_path, 'w') as outfile:
    json.dump(movies_data, outfile, indent=4)

# Log the first 1000 characters of the saved file
with open(output_file_path, 'r') as file:
    logging.info("First 1000 characters of the enriched JSON file:\n" + file.read(1000))

logging.info("JSON file enriched and saved successfully.")
