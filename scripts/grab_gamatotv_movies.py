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
    
    # Find all posts on the current page
    posts = soup.find_all('div', class_='hentry post publish')

    for post in posts:
        # Extract movie title and year
        title_tag = post.find('h1', class_='post-title')
        if title_tag:
            full_title = title_tag.get_text(strip=True)
            
            # Extract the year and remove it from the title
            year = full_title.split('(')[-1].replace(')', '')  # Extracts year
            title = full_title.split('(')[0].strip()  # Removes year from title
            
            # Extract post ID from the div ID
            post_id_raw = post.get('id')
            post_id = post_id_raw.replace('post-', '') if post_id_raw else 'unknown'
            
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
