import json
import os

# Read JSON data from movies.json
with open('data/movies_for_genres.json', 'r') as f:
    data = json.load(f)

# Initialize a new structure to store the genres
genre_based_movies = {}

# Iterate over each movie in the "Movies" list
for movie in data.get('Movies', []):
    genres = movie.get('Genres', "")
    if genres:
        # Split genres by comma and strip whitespace
        genre_list = [genre.strip() for genre in genres.split(',')]
        for genre in genre_list:
            if genre:
                if genre not in genre_based_movies:
                    genre_based_movies[genre] = []
                # Add the movie title under the genre
                genre_based_movies[genre].append({"Title": movie.get("Title")})

# Output the result into a new JSON file
output_file = 'output/genres.json'
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, 'w') as f:
    json.dump(genre_based_movies, f, indent=4)

print(f"Genres processed and saved to {output_file}")
