import json
import requests

# Load your API key
TMDB_API_KEY = '753fba9d8bfbd1068ebd0b4437209a8a'

# Function to fetch movie details from TMDB
def get_movie_details(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Convert genres to a single string
        genres = ", ".join([genre['name'] for genre in data.get('genres', [])])
        return {
            'runtime': data.get('runtime'),
            'genres': genres,
            'year': data.get('release_date', '').split('-')[0] if 'release_date' in data else None
        }
    else:
        return {}

# Load the JSON file from the repository
with open('data/movies_tmdb.json', 'r') as file:
    movies_data = json.load(file)

# Enrich the movies data with additional TMDB info
for movie in movies_data.get('Movies', []):
    if 'TMDB_ID' in movie:
        details = get_movie_details(movie['TMDB_ID'])
        movie.update(details)

# Save the enriched data back to a new JSON file
with open('enriched_movies.json', 'w') as outfile:
    json.dump(movies_data, outfile, indent=4)

print("JSON file enriched and saved as 'enriched_movies.json'.")
