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
    
    # Convert the soup object to a string for substring search
    html_content = str(soup)
    
    # Look for posts that start with '<div id="post-' to extract relevant data
    start_index = 0
    while True:
        # Find the next occurrence of '<div id="post-'
        start_index = html_content.find('<div id="post-', start_index)
        if start_index == -1:
            break
        
        # Extract the substring that contains the post information
        end_index = html_content.find('</div>', start_index)
        post_content = html_content[start_index:end_index]
        
        # Create a soup object for the extracted post content
        post_soup = BeautifulSoup(post_content, 'html.parser')
        
        # Extract post ID
        post_div = post_soup.find('div', id=True)
        post_id_raw = post_div.get('id')
        post_id = post_id_raw.replace('post-', '') if post_id_raw else 'unknown'
        
        # Extract movie title and year
        title_tag = post_soup.find('h1', class_='post-title')
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
        
        # Move the start_index to the end of the current post to find the next one
        start_index = end_index

# Print out the list of movies with IDs
print("Extracted Movies with IDs:")
for movie in movies:
    print(f"ID: {movie['ID']}, Title: {movie['Title']}, Year: {movie['Year']}")
