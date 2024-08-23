import argparse
import requests
from bs4 import BeautifulSoup
import json
import re
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_episode_urls(domain, base_url, query_string, page):
    """Fetches episode URLs from the given page using regex and logs detailed info."""
    # Construct the URL
    if page == 1:
        url = f"{domain}{base_url}?{query_string}"
    else:
        url = f"{domain}{base_url}page/{page}/?{query_string}"
    
    logging.info(f"Fetching URL: {url}")
    
    # Make the HTTP request
    response = requests.get(url)
    logging.info(f"Response status code: {response.status_code}")
    
    # Print the first 5000 characters of the HTML for debugging
    logging.debug(response.text[:5000])
    
    # Find episode URLs using regex
    episode_urls = re.findall(r'https://www\.megatv\.com/tvshows/\d+/epeisodio-\d+', response.text)
    if not episode_urls:
        logging.warning(f"No episode URLs found on page {page}.")
    
    return episode_urls

def scrape_episode_data(episode_url):
    """Scrapes data from an episode page and logs detailed info."""
    try:
        response = requests.get(episode_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.find("meta", property="og:title")["content"].strip()
        description = soup.find("meta", property="og:description")["content"].strip()
        image_url = soup.find("meta", property="og:image")["content"].strip()
        canonical_url = soup.find("link", rel="canonical")["href"]
        
        video_url = ""
        video_div = soup.find("div", {"id": "container_embed"})
        if video_div:
            video_url = video_div.get("data-kwik_source", "").strip()
        
        duration = ""
        duration_match = re.search(r'\b(\d+[:]\d+)\b', description)
        if duration_match:
            duration = duration_match.group()
        
        logging.info(f"Successfully scraped episode data from {episode_url}.")
        
        return {
            "Title": title,
            "Image": image_url,
            "Video": video_url,
            "Description": description,
            "Date": "",
            "Duration": duration,
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
            "Date": "",
            "Duration": "",
            "isUnlocked": False,
            "fetchVideo": False,
            "beforeEnd": 0,
            "Fetch": ""
        }

def generate_json(domain, base_url, query_string, from_page, to_page):
    """Generates a JSON file containing episode data and logs detailed info."""
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
        logging.info(f"Found episode URLs on page {page}: {episode_urls}")
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
    
    logging.info("JSON file 'series.json' has been created successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape Mega TV episodes.')
    parser.add_argument('--domain', type=str, required=True, help='Base domain URL (e.g., https://www.megatv.com)')
    parser.add_argument('--base-url', type=str, required=True, help='Base URL to scrape episodes from')
    parser.add_argument('--query-string', type=str, required=True, help='Query string to append to the base URL')
    parser.add_argument('--from-page', type=str, required=True, help='Starting page number')
    parser.add_argument('--to-page', type=str, required=True, help='Ending page number')
    
    args = parser.parse_args()
    
    generate_json(args.domain, args.base_url, args.query_string, args.from_page, args.to_page)
