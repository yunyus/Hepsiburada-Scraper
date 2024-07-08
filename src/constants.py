# Constants for the scraper

THREAD_COUNT = 64
TIMEOUT = 15
PAGINATION_DEPTH = 20
ALL_CATEGORIES_URL = 'https://www.hepsiburada.com/tum-kategoriler'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://www.hepsiburada.com/'
}

CATEGORY_FILE = './data/fetched_category.txt'
PRODUCT_FILE = './data/fetched_product.txt'
REVIEW_FILE = './data/reviews.csv'
