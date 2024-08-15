import requests
from bs4 import BeautifulSoup
import json
import os

# Base URL to scrape
base_url = 'https://gamatotv.info/el/comedy/'

# TMDB API key and base URL
tmdb_api_key = '753fba9d8bfbd1068ebd0b4437209a8a'
tmdb_base_url = 'https://api.themoviedb.org/3/search/movie'

# Initialize a list to store movie data
movies = []

# Function to search TMDB for a movie and return the first result
def search_tmdb(title, year, post_id):
    params = {
        'query': title,
        'api_key': tmdb_api_key,
        'language': 'el-GR',
        'year': year
    }
    response = requests.get(tmdb_base_url, params=params)
    data = response.json()
    if data['results']:
        # Get the first result
        result = data['results'][0]
        return {
            'TMDB_ID': result['id'],
            'Title': result['title'],  # Use title
            'ImageMain': f"https://www.themoviedb.org/t/p/w600_and_h900_bestv2{result['poster_path']}",
            'Video': post_id,  # Set Video as post ID
            'isUnlocked': True,
            'Fetch': 'GamatoTV'
        }
    return None

# Function to save data to a JSON file
def save_to_file(batch_json, batch_index):
    file_name = f'movies_batch_{batch_index}.json'
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(batch_json)
        print(f'Successfully saved batch {batch_index} to {file_name}')
    except IOError as e:
        print(f"Error saving batch {batch_index} to file: {e}")

# Function to save all movies to JSON files
def save_all_movies(movies):
    batch_size = 50
    for i in range(0, len(movies), batch_size):
        batch = movies[i:i + batch_size]
        batch_index = i // batch_size + 1  # Calculate batch index (1-based)
        batch_json = json.dumps({"Movies": batch}, indent=4, ensure_ascii=False)
        
        # Save the batch JSON to a file
        save_to_file(batch_json, batch_index)

# Main scraping loop
try:
    for page in range(1, 11):
        # Construct the URL for each page
        url = f'{base_url}page/{page}/' if page > 1 else base_url
        
        # Fetch the content of the page
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the main content div
        content_div = soup.find('div', id='content')
        if not content_div:
            print(f"'<div id=\"content\">' not found in the HTML content for page {page}")
            continue
        
        # Find all post entries
        posts = content_div.find_all('div', id=lambda x: x and x.startswith('post-'))
        if not posts:
            print(f"No posts found on page {page}")
            continue
        
        for post in posts:
            # Extract post ID
            post_id = post.get('id').replace('post-', '')
            
            # Extract movie title and year
            title_tag = post.find('h1', class_='post-title')
            if title_tag:
                full_title = title_tag.get_text(strip=True)
                
                # Extract the year and remove it from the title
                year = full_title.split('(')[-1].replace(')', '')  # Extracts year
                title = full_title.split('(')[0].strip()  # Removes year from title
                
                # Search TMDB for the movie
                tmdb_data = search_tmdb(title, year, post_id)
                if tmdb_data:
                    movies.append(tmdb_data)

except Exception as e:
    print(f"An error occurred: {e}")

# Ensure the directory exists and save all movies to JSON files
if not os.path.exists('json_files'):
    os.makedirs('json_files')
    
os.chdir('json_files')

save_all_movies(movies)
