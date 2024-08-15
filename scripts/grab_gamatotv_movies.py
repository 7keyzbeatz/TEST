import requests
from bs4 import BeautifulSoup
import json

# Base URL to scrape
base_url = 'https://gamatotv.info/el/tainies/'

# TMDB API key and base URL
tmdb_api_key = '753fba9d8bfbd1068ebd0b4437209a8a'
tmdb_base_url = 'https://api.themoviedb.org/3/search/movie'

# Initialize a list to store movie data
movies = []

# Function to search TMDB for a movie and return the first result
def search_tmdb(title, year):
    params = {
        'query': title,
        'api_key': tmdb_api_key,
        'language': 'el-GR',
        'year': year
    }
    response = requests.get(tmdb_base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            # Get the first result
            result = data['results'][0]
            return {
                'TMDB_ID': result['id'],
                'Title': result['title'],
                'ImageMain': f"https://www.themoviedb.org/t/p/w600_and_h900_bestv2{result['poster_path']}" if result['poster_path'] else '',
                'Video': None,  # This will be set later
                'isUnlocked': True
            }
    return None

# Loop through pages 1 to 50
for page in range(1, 51):
    # Construct the URL for each page
    url = f'{base_url}page/{page}/' if page > 1 else base_url
    
    # Fetch the content of the page
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve page {page}: Status code {response.status_code}")
        continue
    
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
            tmdb_data = search_tmdb(title, year)
            if tmdb_data:
                tmdb_data['Video'] = post_id  # Set the Video field to the extracted post ID
                tmdb_data['Fetch'] = 'GamatoTV'
                movies.append(tmdb_data)

# Print out the list of movies in JSON format
try:
    movies_json = json.dumps({"Movies": movies}, indent=4, ensure_ascii=False)
    print(movies_json)
except Exception as e:
    print(f"Error serializing JSON: {e}")
