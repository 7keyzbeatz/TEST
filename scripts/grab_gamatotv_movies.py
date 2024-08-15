import requests
from bs4 import BeautifulSoup
import json

# Base URL of the page to scrape
base_url = 'https://gamatotv.info/category/tainies'

# List of URLs to scrape
urls = [base_url, base_url + '/2']

# List to store all movie data
all_movies = []

# Loop through each URL and scrape the data
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all posts
    posts = soup.find_all('div', class_='hentry')
    
    for post in posts:
        # Extract movie title and year
        title = post.find('h1', class_='post-title').get_text(strip=True)
        
        # Extract post ID from the div ID
        post_id = post.get('id').replace('post-', '')
        
        # Append movie data to the list
        all_movies.append({
            'title': title,
            'id': post_id
        })

# Write the data to a JSON file
with open('movie_data.json', 'w') as f:
    json.dump(all_movies, f, ensure_ascii=False, indent=4)

print("Scraping complete. Data saved to movie_data.json")
