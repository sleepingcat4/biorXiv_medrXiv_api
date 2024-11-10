import requests
import csv
import time

API_TEMPLATE = "https://api.biorxiv.org/details/{}/{}-01-01/2024-11-10/{}/json"
OUTPUT_CSV = "biorXiv_license.csv"

def fetch_articles(api_template, server, cursor=0, fetch_all=True):
    all_articles = []
    while True:
        api_url = api_template.format(server, "2013" if server == "biorxiv" else "2019", cursor)
        response = requests.get(api_url)
        data = response.json()

        articles = data.get("collection", [])
        if not articles:
            break

        all_articles.extend(articles)
        cursor += len(articles)
        print(f"Fetched {len(articles)} articles. Total so far: {len(all_articles)}.")

        time.sleep(1)

        if not fetch_all and len(all_articles) >= 100:
            break

    return all_articles

def save_to_csv(data, filename):
    if data:
        headers = list(data[0].keys())
        
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            
            for article in data:
                writer.writerow(article)

if __name__ == "__main__":
    server = input("Do you want to fetch information for bioRxiv or medRxiv? ").strip().lower()
    while server not in ['biorxiv', 'medrxiv']:
        server = input("Please choose either 'biorxiv' or 'medrxiv': ").strip().lower()

    fetch_all = input("Do you want to fetch information for all articles (y/n)? ").strip().lower() == 'y'
    articles = fetch_articles(API_TEMPLATE, server, fetch_all=fetch_all)
    if articles:
        save_to_csv(articles, OUTPUT_CSV)
        print(f"Data successfully saved to {OUTPUT_CSV}")
    else:
        print("No articles found.")
