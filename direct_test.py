import sys
import json
from cli_app import scrape

def main():
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    
    print(f"Testing scraper with URL: {url}")
    result = scrape(url)
    
    if result:
        print("Scraping successful!")
        print(json.dumps(result, indent=2))
    else:
        print("Scraping failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
