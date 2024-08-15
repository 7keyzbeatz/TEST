import requests
from bs4 import BeautifulSoup

# Base URL to scrape
base_url = 'https://gamatotv.info/el/tainies/'

# Initialize a list to store movie data
movies = []

# Loop through pages 1 to 10
for page in range(1, 11):
    # Construct the URL for each page
    if page == 1:
        url = base_url
    else:
        url = f'{base_url}page/{page}/'
    
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
            
            # Add the movie data to the list
            movies.append({
                'ID': post_id,
                'Title': title,
                'Year': year
            })

# Print out the list of movies with IDs
print("Extracted Movies with IDs:")
for movie in movies:
    print(f"ID: {movie['ID']}, Title: {movie['Title']}, Year: {movie['Year']}")
