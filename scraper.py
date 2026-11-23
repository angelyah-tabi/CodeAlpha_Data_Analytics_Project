"""Task 1: Web scraping demo using the practice site quotes.toscrape.com."""
from pathlib import Path
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com/"
OUTPUT = Path("data/quotes_scraped.csv")

def scrape_quotes(max_pages=5):
    rows = []
    url = BASE_URL
    headers = {"User-Agent": "EducationalDataAnalyticsProject/1.0 (learning exercise)"}

    for page in range(max_pages):
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for item in soup.select("div.quote"):
            quote = item.select_one("span.text")
            author = item.select_one("small.author")
            tags = [tag.get_text(strip=True) for tag in item.select("a.tag")]
            rows.append({
                "text": quote.get_text(" ", strip=True) if quote else "",
                "author": author.get_text(strip=True) if author else "Unknown",
                "tags": ", ".join(tags),
                "source_url": url
            })

        next_link = soup.select_one("li.next a")
        if not next_link:
            break
        url = requests.compat.urljoin(url, next_link.get("href", ""))
        time.sleep(1)  # polite delay between page requests

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows).drop_duplicates()
    df.to_csv(OUTPUT, index=False, encoding="utf-8")
    print(f"Saved {len(df)} quotes to {OUTPUT.resolve()}")
    return df

if __name__ == "__main__":
    try:
        result = scrape_quotes(max_pages=5)
        print(result.head())
    except requests.RequestException as exc:
        print("Scraping failed. Check your internet connection and try again.")
        print(f"Details: {exc}")
