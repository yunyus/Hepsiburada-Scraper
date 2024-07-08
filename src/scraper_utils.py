from random import uniform
from time import sleep
import requests
from bs4 import BeautifulSoup
from constants import HEADERS


def initialize_session():
    """Initialize a session for each worker process."""
    global session
    session = requests.Session()
    session.headers.update(HEADERS)


def make_polite_request(url, session, headers, timeout):
    """Make a polite request to a URL."""
    sleep(uniform(3, 10))
    try:
        response = session.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)
    return None


def prepare_soup(url, session):
    """Prepare BeautifulSoup object from a URL."""
    headers = {
        'User-Agent': session.headers['User-Agent'],
        'Accept': 'text/html',
        'Referer': url
    }
    response = make_polite_request(url, session, headers, timeout=15)
    if response:
        return BeautifulSoup(response.text, 'html.parser')
    return None
