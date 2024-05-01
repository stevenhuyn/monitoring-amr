import json as j
import sys
import os
sys.path.append(os.getcwd())
import web_scraper as scrape
import chatgpt_api as api
import output_csv as output
import generate_queries as gen
import utils

'''
TO DO
        Search prompt generation algorithm
        Global Config Text File
        Full on readme explaining stuff
        Call this main file.py file
        Webscraper behave
        Global config file
        Typecheck before csv processing - not corrupt main file
'''

#       IMPORTING, GENERATING & ASSIGNING VARIABLES
# Loading config file
with open(os.path.join("tool","config.json"),"r") as file:
    config_data = j.load(file)
# Query generation configuration
additional_queries = config_data["additional search queries"]
number_of_queries_generated = config_data["number of search queries generated"]
number_of_files_sampled = config_data["number of search query generation files sampled"] #TODO
# Web scraper configuration
number_of_urls_per_page = config_data["maximum number of urls scraped per google page"]
maximum_text_display_length = config_data["maximum text display length"]
max_page_load_wait_time = config_data["maximum page load time"]
text_to_avoid = config_data["text for web scraper to avoid"]
small_time_delay = config_data["scraper small time delay"]
large_time_delay = config_data["scraper large time delay"]
# API-GPT Behaviour
chat_gpt_filter_behaviour = '' #TODO
# Output configuration
new_csv_name = config_data["newly generated csv file name"]
old_csv_name = config_data["continuous csv file name"]
csv_delimiter = config_data["csv delimiter"]
# Using text files
generated_queries = gen.generate_queries(number_of_queries_generated, number_of_files_sampled) if number_of_queries_generated > 0 else []
queries = additional_queries + generated_queries
tracking_variables, specs, formatted_variables = api.get_variables()
synopsis_command = api.get_synopsis_filter_command()
request_example = api.get_request_example() #TODO
request_command = api.get_request_command(tracking_variables, specs)

#       SCRAPING
# Scraping google for sites
scrape.assign_constants(text_to_avoid, small_time_delay, large_time_delay)
search_results = scrape.scrape_google(queries, num_urls= number_of_urls_per_page, max_time = max_page_load_wait_time)  #   Gets websites and urls from specified pages of google
print("\n\n FINISHED SCRAPING GOOGLE \n\n")
[result.display(maximum_text_display_length) for result in search_results]
# Scraping sites
scrape.scrape_sites(search_results, max_time = max_page_load_wait_time)  #   Accesses links and gets text
print("\n\n FINISHED SCRAPING SITES \n\n")
[result.display(maximum_text_display_length) for result in search_results]

#       FILTERING
# Checking blacklist and novel urls

#       API
# Filtering
api.generate_responses(search_results, synopsis_command, chat_gpt_filter_behaviour, 'filter')
utils.process_data(search_results)
[result.display(maximum_text_display_length) for result in search_results]
# Text Generation
api.generate_responses(search_results, request_command, chat_gpt_filter_behaviour,'default')
utils.process_data(search_results,True, tracking_variables, formatted_variables)
[result.display(maximum_text_display_length) for result in search_results]

#       STORING
output.assign_constants(new_csv_name,old_csv_name,csv_delimiter)
output.write_to_csv(search_results)
