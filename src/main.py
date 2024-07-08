#!/usr/bin/env python3

import csv
import requests
import tqdm
from multiprocessing.dummy import Pool
from fake_useragent import UserAgent
from constants import THREAD_COUNT, TIMEOUT, PAGINATION_DEPTH, ALL_CATEGORIES_URL, HEADERS
from scraper import fetch_category_links, fetch_product_links, fetch_and_save_reviews
from scraper_utils import initialize_session
from constants import REVIEW_FILE, PRODUCT_FILE, CATEGORY_FILE


def main(thread_count, timeout, pagination_depth):
    """Main function to orchestrate the scraping process."""

    ua = UserAgent()
    session = requests.Session()
    session.headers.update({
        'User-Agent': ua.random,
        **HEADERS
    })

    print('\nStarting the scraping process...')

    # Step 1: Fetch category links
    categories = fetch_category_links(ALL_CATEGORIES_URL, session)
    with open(CATEGORY_FILE, 'w', encoding="utf-8") as f:
        for category in categories:
            f.write("%s\n" % category)

    print(f'Total number of categories fetched: {len(categories)}')

    # Step 2: Generate paginated category links
    paginated_categories = [
        f"{category}?sayfa={page}" for category in categories for page in range(1, pagination_depth + 1)]

    print('Fetching product links from all categories...')

    # Step 3: Fetch product links
    with Pool(thread_count, initializer=initialize_session) as pool:
        all_product_links = list(tqdm.tqdm(pool.imap(
            fetch_product_links, paginated_categories), total=len(paginated_categories)))

    product_links = [link for sublist in all_product_links for link in sublist]

    with open(PRODUCT_FILE, 'w', encoding="utf-8") as f:
        for product in product_links:
            f.write("%s\n" % product)

    print(f'Total number of products fetched: {len(product_links)}')

    # Step 4: Fetch and save reviews
    with open(REVIEW_FILE, 'w', encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Product', 'Rating', 'Review'])

    print('Fetching reviews for all products...')

    with Pool(thread_count, initializer=initialize_session) as pool:
        for _ in tqdm.tqdm(pool.imap_unordered(fetch_and_save_reviews, product_links), total=len(product_links)):
            pass

    print('\nScraping process completed successfully!')


if __name__ == '__main__':
    main(thread_count=THREAD_COUNT, timeout=TIMEOUT,
         pagination_depth=PAGINATION_DEPTH)
