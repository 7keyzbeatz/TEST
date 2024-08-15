import requests
from bs4 import BeautifulSoup

# URL to scrape
url = 'https://gamatotv.info/el/tainies'

# Fetch the content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize a list to store movie data
movies = []

# Loop through post-1 to post-10
for i in range(1, 11):
    # Construct the class string for each post
    post_class = f'hentry post publish post-{i}'
    
    # Find the post with the specific class
    post = soup.find('div', class_=post_class)
    
    if post:
        # Extract movie title and year
        title_tag = post.find('h1', class_='post-title')
        if title_tag:
            title = title_tag.get_text(strip=True)

            # Extract post ID from the div ID
            post_id = post.get('id').replace('post-', '') if post.get('id') else 'unknown'

            # Add the movie data to the list
            movies.append({
                'id': post_id,
                'title': title,
            })

# Print out the list of movies
print("Extracted Movies:")
for movie in movies:
    print(f"ID: {movie['id']}, Title: {movie['title']}")

# Convert the soup object to a string
html_content = str(soup)

# Find the index of the string '<div id="content">'
start_index = html_content.find('<div id="content">')

# Slice the string from the start_index to the end
if start_index != -1:
    sliced_content = html_content[start_index:]
    print("\nSliced Content Starting from <div id=\"content\">:")
    print(sliced_content[:1000])  # Print the first 1000 characters to avoid overwhelming output
else:
    print("'<div id=\"content\">' not found in the HTML content")

# Parse the sliced content with BeautifulSoup for further processing
if start_index != -1:
    sliced_soup = BeautifulSoup(sliced_content, 'html.parser')
    
    # Example: Find all divs with class 'hentry'
    posts = sliced_soup.find_all('div', class_='hentry')
    
    extracted_data = []

    for post in posts:
        title_tag = post.find('h1', class_='post-title')
        if title_tag:
            title = title_tag.get_text(strip=True)
            year = title.split('(')[-1].replace(')', '')  # Simple year extraction if it follows the title in parentheses
            
            extracted_data.append({
                'Title': title,
                'Year': year
            })

    # Print the extracted data
    print("\nExtracted Data from Sliced Content:")
    for item in extracted_data:
        print(f"Title: {item['Title']}, Year: {item['Year']}")
else:
    print("Skipping extraction from sliced content as the start tag was not found.")
