import requests
from bs4 import BeautifulSoup
import json
import re
import argparse
import os

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Scrape movie data from GamatoTV.')
    parser.add_argument('--base_url', required=True, help='Base URL for scraping')
    parser.add_argument('--start_page', type=int, required=True, help='Start page number')
    parser.add_argument('--end_page', type=int, required=True, help='End page number')
    parser.add_argument('--include_keywords', required=False, help='Comma-separated list of keywords or phrases to include')
    parser.add_argument('--exclude_keywords', required=False, help='Comma-separated list of keywords or phrases to exclude')
    return parser.parse_args()

# Base URL to scrape
def get_base_url(base_url, page):
    return f'{base_url}page/{page}/' if page > 1 else base_url

# TMDB API key and base URL
tmdb_api_key = '753fba9d8bfbd1068ebd0b4437209a8a'
tmdb_base_url = 'https://api.themoviedb.org/3/search/movie'

# Function to search TMDB for a movie and return the first result
def search_tmdb(title, year, post_id, direct_url):
    params = {
        'query': title,
        'api_key': tmdb_api_key,
        'year': year,
        'direct_url': direct_url
    }
    response = requests.get(tmdb_base_url, params=params)
    data = response.json()
    if data['results']:
        result = data['results'][0]
        movie_data = {
            'Fetch': 'GamatoTV',
            'TMDB_ID': result['id'],
            'Title': result['title'],
            'ImageMain': f"https://www.themoviedb.org/t/p/w600_and_h900_bestv2{result['poster_path']}",
            'Video': post_id,
            'DirectVideo': 'null',
            'isUnlocked': True
        }
        print(f"Found movie: {movie_data['Title']} (ID: {movie_data['TMDB_ID']})")
        return movie_data
    print(f"No results found for title: {title} ({year})")
    return None

# Function to fetch the HTML content of a URL
def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

# Function to grab player URLs
def grab_player_urls(input_html):
    if input_html:
        url_pattern = r"http://gmtcloud\.best/\S+(?=\")"
        return re.findall(url_pattern, input_html)
    return []

# Function to grab direct URL
def grab_direct_url(input_html):
    if input_html:
        if "coverapi.store" in input_html:
            return None
        url_pattern = r"http://gmtcloud\.site/video/movies/[\w%\-\.]+\.mp4\?id=\d+"
        match = re.search(url_pattern, input_html)
        if match:
            return match.group()
    return None

# Function to filter by keywords
def keyword_filter(html, include_keywords, exclude_keywords):
    if include_keywords:
        if not all(any(keyword.lower() in html.lower() for keyword in keyword_group.split('|')) for keyword_group in include_keywords):
            print(f"HTML does not contain all required include keywords: {include_keywords}")
            return False
    if exclude_keywords:
        if any(any(keyword.lower() in html.lower() for keyword in keyword_group.split('|')) for keyword_group in exclude_keywords):
            print(f"HTML contains excluded keywords: {exclude_keywords}")
            return False
    return True

# Function to grab streaming URL
def grab_streaming_url(post_id, include_keywords, exclude_keywords):
    url = f"https://gamatotv.info/{post_id}"
    html = fetch_html(url)
    if html:
        if not keyword_filter(html, include_keywords, exclude_keywords):
            print(f"Post {post_id} does not match keyword criteria. Skipping.")
            return None

        player_urls = grab_player_urls(html)
        for player_url in player_urls:
            player_html = fetch_html(player_url)
            if player_html:
                direct_url = grab_direct_url(player_html)
                if direct_url and 'mp4' in direct_url:
                    return direct_url
    return None

# Function to load existing movies from the JSON file
def load_existing_movies(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()  # Read as string for easy checking
    return '{}'

# Function to check if a movie with the given TMDB ID already exists in the JSON file
def movie_exists(tmdb_id, json_str):
    try:
        data = json.loads(json_str)
        return any(movie.get('TMDB_ID') == tmdb_id for movie in data.get("Movies", []))
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return False

# Function to save all movies to a single JSON file
def save_to_file(movies, file_path):
    data = {
        "Main": [
            {
                "Live": True,
                "Video": "",
                "Fetch": "MediaFire"
            }
        ],
        "Movies": movies
    }
    print(f"Attempting to save movies to {file_path}")
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f'Successfully saved all movies to {file_path}')
    except IOError as e:
        print(f"Error saving movies to file: {e}")

# Main scraping loop
def main():
    args = parse_arguments()
    base_url = args.base_url
    start_page = args.start_page
    end_page = args.end_page
    include_keywords = args.include_keywords.split(',') if args.include_keywords else []
    exclude_keywords = args.exclude_keywords.split(',') if args.exclude_keywords else []

    file_path = 'data/movies.json'
    existing_json_str = load_existing_movies(file_path)

    new_movies = []

    try:
        for page in range(start_page, end_page + 1):
            url = get_base_url(base_url, page)
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
                    direct_url = grab_streaming_url(post_id, include_keywords, exclude_keywords)
                    if direct_url:
                        print(f"Valid MP4 URL found: {direct_url}")
                        tmdb_data = search_tmdb(title, year, post_id, direct_url)
                        if tmdb_data:
                            if not movie_exists(tmdb_data['TMDB_ID'], existing_json_str):
                                tmdb_data['DirectVideo'] = direct_url
                                new_movies.append(tmdb_data)
                            else:
                                print(f"Movie with TMDB ID {tmdb_data['TMDB_ID']} already exists. Skipping.")
                    else:
                        print(f"No valid MP4 URL found for post ID: {post_id}")
        if new_movies:
            existing_movies = json.loads(existing_json_str).get("Movies", [])
            existing_movies.extend(new_movies)
            save_to_file(existing_movies, file_path)
        else:
            print("No new movies were found or saved.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
