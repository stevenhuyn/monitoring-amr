import time
from typing import List
from selenium import webdriver
from urllib.parse import parse_qs, parse_qsl, urlencode, urlsplit, urlunsplit
from selenium.webdriver.common.by import By


class SeleniumScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.set_page_load_timeout(5)

    def scrapeGoogle(self, queries: List[str]):
        articleResults = []
        for query in queries:
            searchUrl = SeleniumScraper.buildSearchUrl(query)
            print(searchUrl)
            self.driver.get(searchUrl)
            time.sleep(5)

            search_results = self.driver.find_elements(
                By.XPATH, '//div[@class="m5k28"]'
            )

            for result in search_results:
                frontPage = result.find_element(By.XPATH, './/div[@class="B6pJDd"]')
                title = frontPage.text
                articleUrl = frontPage.find_element(By.CSS_SELECTOR, "a").get_attribute(
                    "href"
                )
                articleResult = ArticleResult(query, articleUrl, title)
                articleResults.append(articleResult)

        self.driver.quit()

        for articleResult in articleResults:
            print(articleResult)

    def buildSearchUrl(query: str) -> str:
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
        queryParams = parse_qs(queryString)
        queryParams.update(searchParams)
        newQueryString = urlencode(queryParams)

        searchUrl = urlunsplit((scheme, netloc, path, newQueryString, fragment))
        return searchUrl


class ArticleResult:
    def __init__(self, query, url, title):
        self.query = query
        self.url = url
        self.title = title

    def __repr__(self):
        return str((self.query, self.url))
