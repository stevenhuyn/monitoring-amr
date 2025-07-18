from my_lib.scraper import ArticlePage, ArticleResult
from openai import OpenAI


class Extractor:
    def __init__(self, systemPrompt, behaviourPrompt, synopsisPrompt):
        self.client = OpenAI()
        self.systemPrompt = systemPrompt
        self.behaviourPrompt = behaviourPrompt
        self.synopsisPrompt = synopsisPrompt

    def extract(
        self, article: ArticlePage
    ) -> str | None:  # TODO create a valid outputs class
        systemPrompt = {"role": "system", "content": self.systemPrompt}
        synopsisCheckPrompt = {
            "role": "user",
            "content": f"{self.synopsisPrompt}\n\n{article.synopsis}",
        }
        extractionPrompt = {
            "role": "user",
            "content": f"{self.behaviourPrompt}\n\n{article.content}",
        }

        synposisCheckOutput = self.client.responses.create(
            model="gpt-4o", input=[systemPrompt, synopsisCheckPrompt]
        )

        if "no" in synposisCheckOutput.output_text.lower():
            return None

        featuresOutput = self.client.responses.create(
            model="gpt-4o", input=[systemPrompt, extractionPrompt]
        )

        print(featuresOutput.output_text)
