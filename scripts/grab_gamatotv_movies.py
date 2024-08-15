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
            else:
                print(f"Warning: Title not found for post-{i} on page-{page}")
        else:
            print(f"Warning: Post-{i} not found on page-{page}")

    # Append the current page's movies to the all_movies list
    all_movies.extend(movies)

# Optional: Deduplicate the movies based on ID
unique_movies = {movie['id']: movie for movie in all_movies}.values()

# Print the unique movies with IDs and cleaned titles (without the year)
print("Unique Movies with Cleaned Titles (No Year):")
for movie in unique_movies:
    try:
        # Print out the movie details
        print(f"ID: {movie['id']}, Title: {movie['title'].split('(')[0].strip()}")
    except KeyError as e:
        print(f"KeyError encountered: {e} in movie entry: {movie}")
