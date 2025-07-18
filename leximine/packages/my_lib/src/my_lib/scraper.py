from typing import List
from selenium import webdriver
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


class SeleniumScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.set_page_load_timeout(5)

    def scrapeGoogle(self, queries: List[str]):
        for query in queries:
            searchParams = {
                # Interface Language
                "hl": "en-IN",
                # Country of the document
                "gl": "IN",
                "ceid": "IN:en",
                "q": query,
            }
            # ?hl=en-IN&gl=IN&ceid=IN%3Aen
            scheme, netloc, path, queryString, fragment = urlsplit(
                "https://news.google.com/search?dog=4"
            )
            queryParams = parse_qsl(queryString)
            queryParams.update(searchParams)
            newQueryString = urlencode(queryParams, doseq=True)

            searchUrl = urlunsplit((scheme, netloc, path, newQueryString, fragment))

            print(searchUrl)
