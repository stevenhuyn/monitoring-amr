from dotenv import load_dotenv
from my_lib import scraper


def main():
    load_dotenv()
    Scraper = scraper.SeleniumScraper()
    Scraper.scrapeGoogle(["antibiotics resistance"])


if __name__ == "__main__":
    main()
