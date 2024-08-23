import argparse
import requests
from bs4 import BeautifulSoup
import json
import re

def get_episode_urls(base_url, page):
    url = base_url if page == 1 else f"{base_url}/page/{page}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    episode_urls = []
    for link in soup.select('.prel.relative-post.blocked a'):
        href = link.get('href')
        if href and href.startswith('/tvshows/'):
            episode_urls.append('https://www.megatv.com' + href)
    
    return episode_urls

def scrape_episode_data(episode_url):
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

def generate_json(base_url, from_page, to_page):
    # Manually defined season
    season = {
        "Title": "1ος Κύκλος",
        "Image": "https://example.com/season1-image.jpg",
        "Year": "2022",
        "isUnlocked": True,
        "Episodes": []
    }

    for page in range(int(from_page), int(to_page) + 1):
        episode_urls = get_episode_urls(base_url, page)
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
    parser.add_argument('--base-url', type=str, required=True, help='Base URL to scrape episodes from')
    parser.add_argument('--from-page', type=str, required=True, help='Starting page number')
    parser.add_argument('--to-page', type=str, required=True, help='Ending page number')
    
    args = parser.parse_args()
    
    generate_json(args.base_url, args.from_page, args.to_page)
