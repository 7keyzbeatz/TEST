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
        result = data['results'][0]
        movie_data = {
            'TMDB_ID': result['id'],
            'Title': result['title'],
            'ImageMain': f"https://www.themoviedb.org/t/p/w600_and_h900_bestv2{result['poster_path']}",
            'Video': post_id,
            'isUnlocked': True,
            'Fetch': 'GamatoTV'
        }
        print(f"Found movie: {movie_data['Title']} (ID: {movie_data['TMDB_ID']})")
        return movie_data
    print(f"No results found for title: {title} ({year})")
    return None

# Function to save all movies to a single JSON file
def save_to_file(movies):
    file_path = 'movies.json'
    print(f"Attempting to save movies to {file_path}")
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump({"Movies": movies}, file, indent=4, ensure_ascii=False)
        print(f'Successfully saved all movies to {file_path}')
    except IOError as e:
        print(f"Error saving movies to file: {e}")

# Main scraping loop
try:
    for page in range(1, 111):
        url = f'{base_url}page/{page}/' if page > 1 else base_url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find('div', id='content')
        if not content_div:
            print(f"'<div id=\"content\">' not found in the HTML content for page {page}")
            continue
        posts = content_div.find_all('div', id=lambda x: x and x.startswith('post-'))
        if not posts:
            print(f"No posts found on page {page}")
            continue
        for post in posts:
            post_id = post.get('id').replace('post-', '')
            title_tag = post.find('h1', class_='post-title')
            if title_tag:
                full_title = title_tag.get_text(strip=True)
                year = full_title.split('(')[-1].replace(')', '')
                title = full_title.split('(')[0].strip()
                print(f"Processing movie: {title} ({year}) with post ID: {post_id}")
                tmdb_data = search_tmdb(title, year, post_id)
                if tmdb_data:
                    movies.append(tmdb_data)
    if movies:
        save_to_file(movies)
    else:
        print("No movies were found or saved.")

except Exception as e:
    print(f"An error occurred: {e}")
