import requests
import json
import time

# Replace with your actual API key
API_KEY = "oulcmpPHppZNamWvRNx8ZsVQixsyaAZXW3qbYmnE0xYVdFhznTIw79nqUm4gXxrH"

# Function to clone a file to another Voe account
def clone_file(file_code):
    url = f"https://voe.sx/api/file/clone?key={API_KEY}&file_code={file_code}&fld_id=65462"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            return data["result"].get("filecode")
        else:
            print(f"Failed to clone file {file_code}: {data.get('message')}")
            return None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def process_json_file(input_file, output_file, batch_size=20, wait_time=15):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    movies = data.get("Movies", [])
    total_movies = len(movies)
    print(f"Total movies to process: {total_movies}")

    for i, movie in enumerate(movies):
        voe_id = movie.get("Voe_ID")
        if voe_id:
            print(f"Processing movie {i + 1}/{total_movies} with Voe_ID: {voe_id}")
            voe_id_backup = clone_file(voe_id)
            if voe_id_backup:
                movie["Voe_ID_Backup"] = voe_id_backup
                print(f"Successfully cloned movie {i + 1}/{total_movies}. New Voe_ID_Backup: {voe_id_backup}")
            else:
                print(f"Failed to clone movie {i + 1}/{total_movies}.")
        else:
            print(f"Movie {i + 1}/{total_movies} does not have a Voe_ID, skipping.")

        remaining_movies = total_movies - (i + 1)
        print(f"Remaining movies: {remaining_movies}")
        
        # Pause after every `batch_size` movies
        if (i + 1) % batch_size == 0:
            print(f"Processed {i + 1} movies. Waiting for {wait_time} seconds to avoid rate limiting...")
            time.sleep(wait_time)
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Processed {total_movies} movies and saved to {output_file}")

if __name__ == "__main__":
    input_file = "data/movies_clone.json"  # The input JSON file
    output_file = "data/movies_with_backup.json"  # The output JSON file
    process_json_file(input_file, output_file)
