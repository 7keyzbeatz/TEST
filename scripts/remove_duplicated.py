import json

def remove_duplicates(input_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    movies = data["Movies"]
    unique_movies = {}
    final_movies = []

    for movie in movies:
        title = movie.get("Title")
        direct_video = movie.get("DirectVideo")

        if not title or not direct_video:
            # Skip movies that don't have both a Title and DirectVideo
            continue

        identifier = (title, direct_video)
        voe_id = movie.get("VOE_ID")
        
        if identifier in unique_movies:
            # If movie with the same Title and DirectVideo already exists
            if voe_id:
                # Replace the movie if the current one has a VOE_ID
                unique_movies[identifier] = movie
        else:
            # Add the movie if it's not in the dictionary yet
            unique_movies[identifier] = movie

    # Convert the dictionary back to a list
    final_movies = list(unique_movies.values())

    # Replace the Movies list with the final cleaned list
    data["Movies"] = final_movies

    # Write the cleaned data back to the file
    with open(input_file, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    remove_duplicates("data/moviesforremoval.json")
