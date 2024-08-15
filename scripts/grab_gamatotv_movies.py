import requests
from bs4 import BeautifulSoup

# Base URL to scrape (we'll append the page number for pages 2-10)
base_url = 'https://gamatotv.info/el/tainies'

# Initialize a list to store movie data from all pages
all_movies = []

# Loop through pages 1 to 10
for page in range(1, 11):
    # Construct the URL for each page
    if page == 1:
        url = base_url
    else:
        url = f'{base_url}/page/{page}'

    # Fetch the content of the page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize a list to store movie data for the current page
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
                post_id_raw = post.get('id')
                post_id = post_id_raw.replace('post-', '') if post_id_raw else 'unknown'

                # Add the movie data to the list
                movies.append({
                    'id': post_id,
                    'title': title,
                })

    # Append the current page's movies to the all_movies list
    all_movies.extend(movies)

    # Convert the soup object to a string
    html_content = str(soup)

    # Find the index of the string '<div id="content">'
    start_index = html_content.find('<div id="content">')

    # Slice the string from the start_index to the end
    if start_index != -1:
        sliced_content = html_content[start_index:]
    else:
        print(f"'<div id=\"content\">' not found in the HTML content of page {page}")

    # Parse the sliced content with BeautifulSoup for further processing
    if start_index != -1:
        sliced_soup = BeautifulSoup(sliced_content, 'html.parser')

        # Find all divs with class 'hentry'
        posts = sliced_soup.find_all('div', class_='hentry')

        extracted_data = []

        for post in posts:
            title_tag = post.find('h1', class_='post-title')
            if title_tag:
                full_title = title_tag.get_text(strip=True)

                # Extract the year and remove it from the title
                year = full_title.split('(')[-1].replace(')', '')  # Extracts year
                title = full_title.split('(')[0].strip()  # Removes year from title

                # Extract post ID from the div ID
                post_id_raw = post.get('id')
                post_id = post_id_raw.replace('post-', '') if post_id_raw else 'unknown'

                extracted_data.append({
                    'ID': post_id,
                    'Title': title,
                    'Year': year
                })

        # Append the extracted data to all_movies list
        all_movies.extend(extracted_data)
    else:
        print(f"Skipping extraction from sliced content as the start tag was not found for page {page}")

# Print out the list of movies with IDs from all pages
print("Extracted Movies with IDs from All Pages:")
for movie in all_movies:
    # Only print unique entries by filtering out duplicates based on ID
    print(f"ID: {movie['id']}, Title: {movie['title']}")

# Optional: Deduplicate the movies based on ID
unique_movies = {movie['id']: movie for movie in all_movies}.values()

# Print the unique movies with IDs and cleaned titles (without the year)
print("\nUnique Movies with Cleaned Titles (No Year):")
for movie in unique_movies:
    print(f"ID: {movie['id']}, Title: {movie['title'].split('(')[0].strip()}")
