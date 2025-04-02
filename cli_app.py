import sys
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import argparse

def scrape(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.text.strip() if soup.title else "No title found"
        
        headings = []
        for h in soup.find_all(['h1', 'h2', 'h3']):
            text = h.get_text().strip()
            if text and len(text) > 3:
                headings.append(text)
        
        paragraphs = []
        for p in soup.find_all('p'):
            text = p.get_text().strip()
            if text and len(text) > 10:
                paragraphs.append(text)
        
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text().strip()
            if text and href and not href.startswith('#'):
                links.append({
                    'text': text,
                    'href': href
                })
        
        meta_data = {}
        for meta in soup.find_all('meta'):
            if meta.get('name') and meta.get('content'):
                meta_data[meta['name']] = meta['content']
        
        data = {
            'url': url,
            'title': title,
            'headings': headings[:5],
            'paragraphs': paragraphs[:5],
            'links': links[:10],
            'meta': meta_data,
            'timestamp': datetime.now().isoformat()
        }
        
        return data
    
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Scrape a website and extract useful information')
    parser.add_argument('url', help='The URL to scrape')
    parser.add_argument('--output', '-o', help='Output file (JSON format)')
    parser.add_argument('--pretty', '-p', action='store_true', help='Pretty print the output')
    
    args = parser.parse_args()
    
    print(f"Scraping {args.url}...")
    data = scrape(args.url)
    
    if not data:
        print("Failed to scrape the URL.")
        return 1
    
    if args.output:
        with open(args.output, 'w') as f:
            if args.pretty:
                json.dump(data, f, indent=2)
            else:
                json.dump(data, f)
        print(f"Data saved to {args.output}")
    else:
        if args.pretty:
            print(json.dumps(data, indent=2))
        else:
            print(json.dumps(data))
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
