import sys
import os
sys.path.append(os.getcwd())
import web_scraper as scrape
import chatgpt_api as api
import output_csv as output
import generate_queries as gen

def process_data():
    global search_results
    for i, result in enumerate(search_results):
        if not(result.contains_AMR):
            search_results.pop(i)

'''
TO DO
Keyword engineering.
One-shot learning.
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
chat_gpt_filter_behaviour = '' #TODO

#       GENERATING VARIABLES
generated_queries = gen.generate_queries(number_of_queries_generated, number_of_files_sampled) if number_of_queries_generated > 0 else []
queries = additional_queries + generated_queries
tracking_variables = api.get_variables()
synopsis_command = api.get_synopsis_filter_command()
request_example = api.get_request_example() #TODO
request_command = api.get_request_command(tracking_variables)

#       SCRAPING
search_results = scrape.scrape_google(queries, num_urls= number_of_urls_per_page, 
        num_pages = number_of_pages_to_scrape)  #   Gets websites and urls from specified pages of google
[result.display(maximum_text_display_length) for result in search_results]
scrape.scrape_sites(search_results)  #   Accesses links and gets text
[result.display(maximum_text_display_length) for result in search_results]

#       FILTERING

#       API
# Filtering
api.generate_responses(search_results, synopsis_command, chat_gpt_filter_behaviour, 'filter')
process_data()
# Text Generation
api.generate_responses(search_results, request_command, chat_gpt_filter_behaviour, 'default')
process_data()
#       STORING

# #       OUTPUTTING TO CSV
# output.write_to_csv(search_results)