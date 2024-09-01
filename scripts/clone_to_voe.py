import requests
import json

# Replace with your actual API key
API_KEY = "oulcmpPHppZNamWvRNx8ZsVQixsyaAZXW3qbYmnE0xYVdFhznTIw79nqUm4gXxrH"

# Function to clone a file to another Voe account
def clone_file(file_code):
    url = f"https://voe.sx/api/file/clone?key={API_KEY}&file_code={file_code}&fld_id=65461"
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

def process_json_file(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    movies = data.get("Movies", [])
    for movie in movies:
        voe_id = movie.get("Voe_ID")
        if voe_id:
            voe_id_backup = clone_file(voe_id)
            if voe_id_backup:
                movie["Voe_ID_Backup"] = voe_id_backup
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Processed {len(movies)} movies and saved to {output_file}")

if __name__ == "__main__":
    input_file = "data/movies_clone.json"  # The input JSON file
    output_file = "data/movies_with_backup.json"  # The output JSON file
    process_json_file(input_file, output_file)
