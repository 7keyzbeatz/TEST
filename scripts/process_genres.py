import json
import os

# Define the input and output file paths
input_file = 'data/movies_for_genres.json'
output_file = 'output/genres.json'

# Read JSON data from the input file
with open(input_file, 'r') as f:
    data = json.load(f)

# Process each movie to transform the Genres field
for movie in data.get('Movies', []):
    genres = movie.get('Genres', "")
    # Split the genres and create a list of objects with "Title" keys
    genre_list = [{"Title": genre.strip()} for genre in genres.split(',') if genre.strip()]
    # Update the Genres field with the new format
    movie['Genres'] = genre_list

# Create output directory if it doesn't exist
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Write the modified data back to a new JSON file
with open(output_file, 'w') as f:
    json.dump(data, f, indent=4)

print(f"Processed movies saved to {output_file}")
