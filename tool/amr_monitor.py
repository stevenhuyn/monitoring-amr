import sys
import os
sys.path.append(os.getcwd())
import web_scraper as scrape
import chatgpt_api as api
import output_csv as output


queries = ["machine learning"]
number_of_pages_to_scrape = 1 #TODO, still need to implement
number_of_urls_per_page = 3
maximum_text_display_length = 1000

search_results = scrape.scrape_google(queries, num_urls= number_of_urls_per_page, 
        num_pages = number_of_pages_to_scrape)  #   Gets websites and urls from specified pages of google
scrape.scrape_sites(search_results)  #   Accesses links and gets text
print("Search Results:")
for i, result in enumerate(search_results):
    print(f"Result {i+1}")
    result.display(maximum_text_display_length)