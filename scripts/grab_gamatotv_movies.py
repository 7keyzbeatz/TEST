import requests
from bs4 import BeautifulSoup
import json

# Base URLs of the pages to scrape
base_url = 'https://gamatotv.info/category/tainies'
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
        title_tag = post.find('h1', class_='post-title')
        
        # Check if the title tag is found
        if title_tag:
            title = title_tag.get_text(strip=True)
        else:
            # Skip this post if no title is found
            continue
        
        # Extract post ID from the div ID
        post_id = post.get('id').replace('post-', '') if post.get('id') else 'unknown'
        
        # Append movie data to the list
        all_movies.append({
            'title': title,
            'id': post_id
        })

# Convert the list of movies to JSON and print it
json_output = json.dumps(all_movies, ensure_ascii=False, indent=4)
print(json_output)
