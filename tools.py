import re
import requests
from bs4 import BeautifulSoup




def is_product_link(url):
    pattern = re.compile(r'https?://(?:www\.)?basalam\.com/([^/]+)/product/(\d+)')
    return bool(pattern.match(url))

def extract_shop_link(product_url):
    shop_link = re.sub(r'/product/\d+', '', product_url)
    return shop_link

def is_shop_active(url):

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    inactive = soup.select_one(
        "div.bs-container div.oLb_LX img.MAsCzs[alt='این غرفه فعلا غیرفعاله']"
    )
    return inactive is None
