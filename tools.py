from firecrawl import FirecrawlApp
import re


def is_product_link(url):
    pattern = re.compile(r'https?://(?:www\.)?basalam\.com/([^/]+)/product/(\d+)')
    return bool(pattern.match(url))

def extract_shop_link(product_url):
    shop_link = re.sub(r'/product/\d+', '', product_url)
    return shop_link
