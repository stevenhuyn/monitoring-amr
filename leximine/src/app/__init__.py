from dotenv import load_dotenv
from my_lib.scraper import SeleniumScraper, ArticleLink, ArticlePage
from my_lib.extractor import Extractor


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

    exampleArticlePage = ArticlePage(
        ArticleLink("", "", "SUPER MICROBE FOUND IN DELHI"),
        "BREAKING NEWS, SUPER MICROBE FOUND IN DELHI, 1000 hospitalised!",
    )

    articlePages.insert(0, exampleArticlePage)

    for articlePage in articlePages:
        print(extractor.extract(articlePage))


if __name__ == "__main__":
    main()
