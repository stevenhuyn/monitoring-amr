from dotenv import load_dotenv
from core.scraper import SeleniumScraper, ArticleLink, ArticlePage
from core.extractor import Extractor


def main():
    load_dotenv()
    scraper = SeleniumScraper()
    articlePages = scraper.scrapeGoogle(["antibiotics resistance"])

    systemPrompt = None
    with open("./packages/my_lib/src/my_lib/prompts/system.txt", "r") as f:
        systemPrompt = f.read()

    filterPrompt = None
    with open("./packages/my_lib/src/my_lib/prompts/filter.txt", "r") as f:
        filterPrompt = f.read()

    extractPrompt = None
    with open("./packages/my_lib/src/my_lib/prompts/extract.txt", "r") as f:
        extractPrompt = f.read()

    extractor = Extractor(systemPrompt, extractPrompt, filterPrompt)

    for articlePage in articlePages:
        print(extractor.extract(articlePage))


if __name__ == "__main__":
    main()
