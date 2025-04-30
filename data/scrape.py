import requests
from bs4 import BeautifulSoup
import csv
import random
import time

BASE_URL = "http://books.toscrape.com/"
CATALOGUE_URL = "http://books.toscrape.com/catalogue/"

def scrape_books():
    books = []
    url = BASE_URL + "catalogue/page-1.html"  # Start directly at page 1 in /catalogue/

    while url:
        print(f"Scraping {url}...")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all book containers
        articles = soup.find_all('article', class_='product_pod')

        for article in articles:
            title = article.h3.a['title']
            price = article.find('p', class_='price_color').text.strip()
            availability = article.find('p', class_='instock availability').text.strip()

            books.append({
                "Title": title,
                "Price": price,
                "Availability": availability
            })

        # Find 'next' page
        next_button = soup.find('li', class_='next')
        if next_button:
            next_page_url = next_button.a['href']
            url = CATALOGUE_URL + next_page_url  # Always build from catalogue base
        else:
            url = None

        time.sleep(1)  # Be polite

    return books

def split_books(books):
    random.shuffle(books)  # Shuffle to randomize assignment
    half = len(books) // 2
    vendor_a = books[:half]
    vendor_b = books[half:]
    return vendor_a, vendor_b

def save_to_csv(books, filename):
    keys = books[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(books)

if __name__ == "__main__":
    all_books = scrape_books()
    vendor_a_books, vendor_b_books = split_books(all_books)

    save_to_csv(vendor_a_books, 'vendor_a_books.csv')
    save_to_csv(vendor_b_books, 'vendor_b_books.csv')

    print(f"\nScraped {len(all_books)} books total!")
    print(f"Vendor A: {len(vendor_a_books)} books saved to 'vendor_a_books.csv'.")
    print(f"Vendor B: {len(vendor_b_books)} books saved to 'vendor_b_books.csv'.")
    print("✅ Scraping terminé, fichiers 'vendor_a_books.csv' et 'vendor_b_books.csv' créés !")
# This code scrapes book data from the website, splits the data into two random sets, and saves them to separate CSV files.