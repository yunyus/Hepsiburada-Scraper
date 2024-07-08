import csv
import json
from multiprocessing.dummy import Semaphore
from scraper_utils import prepare_soup
import requests
from constants import REVIEW_FILE, PRODUCT_FILE, CATEGORY_FILE

semaphore = Semaphore(3)


def fetch_category_links(home_url, session):
    """Fetch category links from the homepage."""
    categories = []
    soup = prepare_soup(home_url, session)
    if soup:
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '-c-' in href:
                if 'https://' not in href:
                    href = 'https://www.hepsiburada.com' + href.split('?')[0]
                categories.append(href)
    else:
        print('Failed to scrape categories!')
    return categories


def fetch_product_links(category_url):
    """Fetch product links from a category page."""
    products = []
    session = requests.Session()
    soup = prepare_soup(category_url, session)
    if soup:
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '-p-' in href:
                if 'https://' not in href:
                    href = 'https://www.hepsiburada.com' + \
                        href.split('?')[0] + '-yorumlari'
                products.append(href)
    return products


def fetch_and_save_reviews(product_url):
    """Fetch and save reviews from a product page."""
    session = requests.Session()
    soup = prepare_soup(product_url, session)
    if soup:
        script_tag = soup.find('script', type='application/ld+json')
        if script_tag:
            try:
                reviews_data = json.loads(script_tag.string)
                if isinstance(reviews_data, list):
                    for review in reviews_data:
                        review_body = review.get(
                            'reviewBody', '').strip().replace('\n', ' ')
                        review_rating = review.get(
                            'reviewRating', {}).get('ratingValue', 0)
                        review_product = review.get(
                            'itemReviewed', {}).get('name', '')
                        row = [review_product, review_rating, review_body]
                        semaphore.acquire()
                        with open(REVIEW_FILE, 'a', encoding="utf-8", newline='') as wFile:
                            writer = csv.writer(wFile)
                            writer.writerow(row)
                        semaphore.release()
            except json.JSONDecodeError:
                print("Error decoding JSON from: " + product_url)
