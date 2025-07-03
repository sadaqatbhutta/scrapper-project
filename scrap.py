import requests
from bs4 import BeautifulSoup
import csv
import json

url = "https://en.wikipedia.org/wiki/History_of_blogging"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, 'lxml')

    # Scrape hidden categories
    categories = []
    for item in soup.select('.mw-hidden-catlinks a'):
        categories.append({
            "text": item.text.strip(),
            "href": item['href']
        })

    # Save to CSV
    with open('categories.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['text', 'href']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in categories:
            writer.writerow(item)

    # Save to JSON
    with open('categories.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(categories, jsonfile, indent=2, ensure_ascii=False)

    print("✅ Scraping done! Data saved to categories.csv and categories.json")

else:
    print(f"❌ Failed to fetch page. Status code: {response.status_code}")
