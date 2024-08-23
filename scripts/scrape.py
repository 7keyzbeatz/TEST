import argparse
import requests
from bs4 import BeautifulSoup
import re
import json
import html

def get_episode_urls(domain, base_url, query_string, page):
    # Construct the URL
    if page == 1:
        url = f"{domain}{base_url}?{query_string}"
    else:
        url = f"{domain}{base_url}page/{page}/?{query_string}"
    
    print(f"Fetching URL: {url}")
    
    # Make the HTTP request
    response = requests.get(url)
    print(f"Response status code: {response.status_code}")
    
    # Check if the response is successful
    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return []

    # Print the first 5000 characters of the HTML for debugging
    print(response.text[:5000])
    
    # Define the regex pattern for episode URLs
    pattern = r'https:\/\/www\.megatv\.com\/tvshows\/\d+\/epeisodio-\d+-\d+\/'

    #pattern = r'https:\/\/www\.megatv\.com\/tvshows\/\d+\/[a-zA-Z0-9-]+\/'

    pattern = r'https:\/\/www\.megatv\.com\/tvshows\/\d+\/episode-\d{3}-\d+\/'
    
    # Find all matches in the HTML content
    episode_urls = re.findall(pattern, response.text)
    
    return episode_urls

def scrape_episode_data(episode_url):
    response = requests.get(episode_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract title
    title_tag = soup.find("meta", property="og:title")
    if title_tag:
        title = title_tag["content"].strip()
        # Clean title to format: Επεισόδιο 1
        title = re.sub(r'\s*\|\s*MEGA TV$', '', title)  # Remove the "| MEGA TV" part
        title = re.sub(r'Επεισόδιο:\s*', 'Επεισόδιο ', title)  # Replace "Επεισόδιο:" with "Επεισόδιο "
    else:
        title = "Title Not Found"

    # Extract description
    description_div = soup.find("div", id="EpisodeSum")
    if description_div:
        description_parts = []
        for p in description_div.find_all("p"):
            # Collect all <p> tags and filter out non-description parts
            text = p.get_text(strip=True)
            if text and not p.find("strong"):
                description_parts.append(text)
        description = ' '.join(description_parts)
        description = html.unescape(description)  # Decode HTML entities
    else:
        description = "Description Not Found"

    # Extract image URL
    image_tag = soup.find("meta", property="og:image")
    image_url = image_tag["content"].strip() if image_tag else "Image Not Found"

    # Extract video URL using regex on entire HTML content
    video_url = ""
    video_div = soup.find("div", {"id": "container_embed"})
    if video_div:
        html_content = str(video_div)  # Convert div content to string
        m3u8_match = re.search(r'https://[^\s]+\.m3u8', html_content)
        if m3u8_match:
            video_url = m3u8_match.group().strip()

    # Extract date
    date_span = soup.find("span", id="currentdate")
    date = date_span.get_text(strip=True).split()[0] if date_span else "Date Not Found"

    # Extract duration (if available in description)
    duration = ""
    duration_match = re.search(r'\b(\d+[:]\d+)\b', description)
    if duration_match:
        duration = duration_match.group()

    return {
        "Title": title if title else "Title Not Found",
        "Image": image_url if image_url else "Image Not Found",
        "Video": video_url if video_url else "Video Not Found",
        "Description": description if description else "Description Not Found",
        "Date": date if date else "Date Not Found",
        "Duration": duration if duration else "Duration Not Found",
        "isUnlocked": True,
        "fetchVideo": False,
        "beforeEnd": 0,
        "Fetch": ""
    }

def generate_json(domain, base_url, query_string, from_page, to_page):
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
        print(f"Found episode URLs on page {page}: {episode_urls}")
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
