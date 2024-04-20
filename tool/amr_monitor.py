import sys
import os
sys.path.append(os.getcwd())
import web_scraper as scrape
import chatgpt_api as api
import output_csv as output
import generate_queries as gen

'''
TO DO
        Prompt Engineering.
        Prompt Processing.
        Using the synopsis.
Keyword engineering.
One-shot learning.
Blacklist
'''
#       USER VARIABLES
# Queries
additional_queries = ['machine learning']
number_of_queries_generated = 0
number_of_files_sampled = 3
# Scraping
number_of_pages_to_scrape = 1 #TODO, still need to implement
number_of_urls_per_page = 3
maximum_text_display_length = 500
# API-GPT Behaviour
chatgpt_behaviour = 'You are my assistant - you are polite and concise.'
chatGPT_command = 'Please summarize this article in no more than two sentences.'

#       GENERATING VARIABLES
generated_queries = gen.generate_queries(number_of_queries_generated, number_of_files_sampled) if number_of_queries_generated > 0 else []
queries = additional_queries + generated_queries

#       SCRAPING
search_results = scrape.scrape_google(queries, num_urls= number_of_urls_per_page, 
        num_pages = number_of_pages_to_scrape)  #   Gets websites and urls from specified pages of google
[result.display(maximum_text_display_length) for result in search_results]
scrape.scrape_sites(search_results)  #   Accesses links and gets text
[result.display(maximum_text_display_length) for result in search_results]

#       FILTERING

#       API

#       STORING

# #       SEEING IF NEW and or RELEVANT
# #TODO

# #       SENDING TO CHATGPT
# api.generate_responses(search_results,chatGPT_command,chatgpt_behaviour)

# #       OUTPUTTING TO CSV
# output.write_to_csv(search_results)