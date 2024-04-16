import sys
import os
sys.path.append(os.getcwd())
import web_scraper as scrape
import chatgpt_api as api
import output_csv as output

queries = ["machine learning"] #TODO NEED TO WORK WITH IMAGE BASED PAGES
number_of_pages_to_scrape = 1 #TODO, still need to implement
number_of_urls_per_page = 2
maximum_text_display_length = 500

chatgpt_behaviour = 'You are my assistant - you are polite and concise.'
chatGPT_command = 'Please summarize this article in no more than two sentences.'

#       SCRAPING
search_results = scrape.scrape_google(queries, num_urls= number_of_urls_per_page, 
        num_pages = number_of_pages_to_scrape)  #   Gets websites and urls from specified pages of google
[result.display(maximum_text_display_length) for result in search_results]
scrape.scrape_sites(search_results)  #   Accesses links and gets text

#       SEEING IF NEW and or RELEVANT
#TODO

#       SENDING TO CHATGPT
api.generate_responses(search_results,chatGPT_command,chatgpt_behaviour)

#       OUTPUTTING TO CSV
output.write_to_csv(search_results)