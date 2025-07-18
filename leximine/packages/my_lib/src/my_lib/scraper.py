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
        articleLinks = []
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
                synopsis = result.find_element(
                    By.XPATH, './/div[@data-snf="nke7rc"]'
                ).text

                articleLink = ArticleLink(query, articleUrl, title, synopsis)
                articleLinks.append(articleLink)

        self.driver.quit()

        articlePages = []
        for articleLink in articleLinks:
            self.driver.get(articleLink.url)
            time.sleep(5)
            pSelectors = self.driverdriver.find_elements(By.XPATH, "//body//p")
            listSelectors = self.driverdriver.find_elements(
                By.XPATH, "//body//ol | //body//ul"
            )
            text = "\n".join([item.text for item in pSelectors + listSelectors])
            if len(text) < 400:
                text = "\n".join(
                    [
                        div.text
                        for div in self.driver.find_elements(By.XPATH, "//body//div")
                    ]
                )
            articlePages.append(ArticlePage(articleLink, text))

        self.driver.quit()

        return articlePages

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


class ArticleLink:
    def __init__(self, query, url, title, synopsis):
        self.query = query
        self.url = url
        self.title = title
        self.synopsis = synopsis

    def __repr__(self):
        return str((self.query, self.url))


class ArticlePage:
    def __init__(self, articleLink, synopsis, content):
        self.query = articleLink.query
        self.url = articleLink.url
        self.title = articleLink.title
        self.synopsis = articleLink.synopsis
        self.content = content

    def __repr__(self):
        return str((self.query, self.url))
