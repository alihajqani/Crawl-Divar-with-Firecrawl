from firecrawl import FirecrawlApp
import re

from tools import is_product_link, extract_shop_link


shop_links = []
product_links = []


app = FirecrawlApp(api_key="fc-****-**-**-**-**")


map_results = app.map_url('https://basalam.com')
all_links = map_results.links

for link in all_links:
    if is_product_link(link):
        product_links.append(link)
        shop_links.append(extract_shop_link(link))
