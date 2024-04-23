import sys
import os
sys.path.append(os.getcwd())
import web_scraper as scrape
import chatgpt_api as api
import output_csv as output
import generate_queries as gen

def process_data(process_variables = False, variables = None, formatted_variables = None):
    global search_results
    for i, result in enumerate(search_results):
        if not(result.contains_AMR):
            search_results.pop(i)
    
    if process_variables:    
        for result in search_results:
            processing_text = result.text_response.split('\n')
            for i,variable in enumerate(variables):
                for text in processing_text:
                    if variable +':' in text.lower():
                        result.set_variable(formatted_variables[i],text.split(':')[1].strip())
                        continue
'''
TO DO
Keyword engineering.
One-shot learning.
'''
#       USER VARIABLES
# Queries
additional_queries = ['Over half of antibiotics prescribed in India cause antimicrobial resistance', 'AMR risk surged after pandemic: study','Antibiotic resistance is a growing threat — is climate change making it worse?','The paradox of antimicrobial resistance in India']
number_of_queries_generated = 0
number_of_files_sampled = 3
# Scraping
number_of_pages_to_scrape = 1 #TODO, still need to implement
number_of_urls_per_page = 2
maximum_text_display_length = 500
max_page_load_wait_time = 30
# API-GPT Behaviour
chat_gpt_filter_behaviour = '' #TODO

#       GENERATING VARIABLES
generated_queries = gen.generate_queries(number_of_queries_generated, number_of_files_sampled) if number_of_queries_generated > 0 else []
queries = additional_queries + generated_queries
tracking_variables, specs, formatted_variables = api.get_variables()
synopsis_command = api.get_synopsis_filter_command()
request_example = api.get_request_example() #TODO
request_command = api.get_request_command(tracking_variables, specs)

print(generated_queries, end = '\n\n')
print(tracking_variables, end = '\n\n')
print(specs, end = '\n\n')
print(formatted_variables, end = '\n\n')
print(synopsis_command, end = '\n\n')
print(request_command, end = '\n\n')

#       SCRAPING
search_results = scrape.scrape_google(queries, num_urls= number_of_urls_per_page, 
        num_pages = number_of_pages_to_scrape, max_time = max_page_load_wait_time)  #   Gets websites and urls from specified pages of google
print("\n\n FINISHED SCRAPING GOOGLE \n\n")
[result.display(maximum_text_display_length) for result in search_results]
scrape.scrape_sites(search_results, max_time = max_page_load_wait_time)  #   Accesses links and gets text
print("\n\n FINISHED SCRAPING SITES \n\n")
[result.display(maximum_text_display_length) for result in search_results]

#       FILTERING

#       API
# Filtering
api.generate_responses(search_results, synopsis_command, chat_gpt_filter_behaviour, 'filter')
process_data()
[result.display(maximum_text_display_length) for result in search_results]
# Text Generation
api.generate_responses(search_results, request_command, chat_gpt_filter_behaviour,'default')
process_data(True, tracking_variables, formatted_variables)
[result.display(maximum_text_display_length) for result in search_results]
#       STORING
output.write_to_csv(search_results)
