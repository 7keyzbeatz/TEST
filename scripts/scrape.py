import argparse
import requests
from bs4 import BeautifulSoup
import json
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_episode_urls(domain, base_url, query_string, page):
    """Fetch episode URLs from the specified page."""
    if page == 1:
        url = f"{domain}{base_url}?{query_string}"
    else:
        url = f"{domain}{base_url}page/{page}/?{query_string}"
    
    logging.info(f"Fetching URL: {url}")
    
    try:
        # Make the HTTP request
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        logging.info(f"Response status code: {response.status_code}")

        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Debug output of the first 5000 characters of the HTML
        logging.debug(f"HTML content preview: {response.text[:5000]}")
        
        episode_urls = []
        
        # Use a CSS selector to find episode links
        for link in soup.select('.prel.relative-post.blocked a'):
            href = link.get('href')
            if href and href.startswith('/tvshows/'):
                episode_urls.append('https://www.megatv.com' + href)
        
        logging.info(f"Found episode URLs: {episode_urls}")
        return episode_urls
    except Exception as e:
        logging.error(f"Error fetching episode URLs: {e}")
        return []

def scrape_episode_data(episode_url):
    """Scrapes data from an episode page and logs detailed info."""
    try:
        response = requests.get(episode_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the title
        title_meta = soup.find("meta", property="og:title")
        title = title_meta["content"].strip() if title_meta else "Unknown Title"

        # Extract the date
        date_span = soup.find("span", id="currentdate")
        date = date_span.get_text(strip=True) if date_span else "No Date Available"

        # Extract the M3U8 URL using regex
        video_div = soup.find("div", id="container_embed")
        video_url = ""
        if video_div:
            # Get the HTML content of the div to apply regex
            video_html = str(video_div)
            # Regex to find the M3U8 URL
            match = re.search(r'data-kwik_source="([^"]+)"', video_html)
            if match:
                video_url = match.group(1).strip()

        # Extract the description from the div with id "EpisodeSum"
        description_div = soup.find("div", id="EpisodeSum")
        description = ""
        if description_div:
            # Get all <p> tags and concatenate their text
            paragraphs = description_div.find_all("p")
            description = ' '.join(p.get_text(strip=True) for p in paragraphs)

        logging.info(f"Successfully scraped episode data from {episode_url}. Title: {title}, Date: {date}, Video URL: {video_url}, Description: {description}")

        return {
            "Title": title,
            "Image": "",  # Placeholder as image extraction was not requested
            "Video": video_url,
            "Description": description,
            "Date": date,
            "Duration": "",  # Placeholder if duration extraction is not applicable
            "isUnlocked": True,
            "fetchVideo": False,
            "beforeEnd": 0,
            "Fetch": ""
        }
    except Exception as e:
        logging.error(f"Failed to scrape data from {episode_url}: {e}")
        return {
            "Title": "Unknown",
            "Image": "",
            "Video": "",
            "Description": "Failed to scrape",
            "Date": "Unknown",
            "Duration": "",
            "isUnlocked": False,
            "fetchVideo": False,
            "beforeEnd": 0,
            "Fetch": ""
        }

def generate_json(domain, base_url, query_string, from_page, to_page):
    """Generates JSON file with episode data."""
    # Manually defined season
    season = {
        "Title": "1ος Κύκλος",
        "Image": "https://example.com/season1-image.jpg",
        "Year": "2022",
        "isUnlocked": True,
        "Episodes": []
    }

    for page in range(int(from_page), int(to_page) + 1):
        episode_urls = get_episode_urls(domain, base_url, query_string, page)
        for url in episode_urls:
            episode_data = scrape_episode_data(url)
            season["Episodes"].append(episode_data)

    series_data = {
        "Main": [
            {
                "Live": True,
                "Video": "",
                "Fetch": "MediaFire"
            }
        ],
        "Series": [season]
    }

    with open('series.json', 'w', encoding='utf-8') as f:
        json.dump(series_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape Mega TV episodes.')
    parser.add_argument('--domain', type=str, required=True, help='Base domain URL (e.g., https://www.megatv.com)')
    parser.add_argument('--base-url', type=str, required=True, help='Base URL to scrape episodes from')
    parser.add_argument('--query-string', type=str, required=True, help='Query string to append to the base URL')
    parser.add_argument('--from-page', type=str, required=True, help='Starting page number')
    parser.add_argument('--to-page', type=str, required=True, help='Ending page number')
    
    args = parser.parse_args()
    
    generate_json(args.domain, args.base_url, args.query_string, args.from_page, args.to_page)
