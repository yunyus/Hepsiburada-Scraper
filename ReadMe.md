# Review Scraper for Hepsiburada

This repository contains a web scraper to fetch product categories, product links, and reviews from Hepsiburada. The scraper uses multiple threads for efficiency and stores the fetched data in text and CSV files.

## Project Structure

```
review_scraper/
│
├── data/
│   ├── fetched_category.txt    # Fetched category links
│   ├── fetched_product.txt     # Fetched product links
│   ├── reviews.csv             # Fetched reviews
├── src/
│   ├── constants.py            # Contains constants used in the scraper
│   ├── main.py                 # Main script to run the scraping process
│   ├── scraper_utils.py        # Utility functions for the scraper
│   ├── scraper.py              # Functions to fetch category links, product links, and reviews
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## Setup

1. Clone the repository:

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Scraper

To run the scraper, execute the following command:

```
python src/main.py
```

This will start the scraping process, which involves:

1. Fetching category links from Hepsiburada.
2. Generating paginated category links.
3. Fetching product links from all categories.
4. Fetching and saving reviews for all products.

**Note:** The fetched category links (`fetched_category.txt`) and product links (`fetched_product.txt`) are already provided in the `data` folder. If you want to use these pre-fetched links, make sure to comment out the corresponding parts in `main.py` where these links are generated. If you prefer to fetch these links yourself, delete the existing files.

### Potential Issues

- You may encounter forbidden errors while fetching some products due to the usage of multiple threads. However, the scraper fetches most of the products successfully.

### File Descriptions

- **constants.py**: Contains constants used in the scraper such as thread count, timeout settings, URLs, and file paths.
- **main.py**: The main script to orchestrate the scraping process.
- **scraper_utils.py**: Utility functions for making polite requests and preparing BeautifulSoup objects.
- **scraper.py**: Functions to fetch category links, product links, and reviews.

### Data Files

- **fetched_category.txt**: Stores the fetched category links.
- **fetched_product.txt**: Stores the fetched product links.
- **reviews.csv**: Stores the fetched reviews in CSV format.

Make sure to update the constants in `constants.py` as needed, particularly the file paths and URLs.

This project is built upon the the following project: https://github.com/0x01h/hepsiburada-review-scraper
