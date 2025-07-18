from my_lib import scraper


def main():
    Scraper = scraper.SeleniumScraper()
    Scraper.scrapeGoogle(["antibiotics"])


if __name__ == "__main__":
    main()
