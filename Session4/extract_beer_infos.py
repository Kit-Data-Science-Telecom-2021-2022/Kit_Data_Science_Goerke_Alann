import requests
import re
from bs4 import BeautifulSoup

def extract_beer_infos(url):
    """Returns a dictionnary containing the name, the note, the price
    and the volume of a beer.

    Arguments:
    url (type: str): the url of the beer web page.
    """
    r = requests.get(url)  # Extract informations from a given url

    content = r.content.decode('utf-8')  # Transform content into a str

    soup = BeautifulSoup(content)  # Set up of the BeautifulSoup method

    biere = soup.find('div', {'class': "product-detail-info-row mobile-header-details"})  # Find the root

    price_content = soup.find('script', {'type': 'application/ld+json'}).contents[0]
    rx = re.compile('"price": "([^<]+)",')
    match_price = rx.search(price_content)  # Use of regex method to find the beer price

    infos = {
        'name': biere.find('h1').text,
        'note': int(biere.find('div', {'class': 'stars'}).attrs['data-percent']),
        'price': float(match_price.group(1)),
        'volume': int(biere.find('span').text.split(' | ')[-1][:-len(' cl')]),
    }

    return infos