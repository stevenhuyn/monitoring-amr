from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

TEXT_TO_AVOID = ['scholarly articles' , 'people also ask', 'local results']
SMALL_TIME_DELAY = 5
LARGE_TIME_DELAY = SMALL_TIME_DELAY * 2

class search_result:
    def __init__(self,query,website_dir,url,title,synopsis):
        self.query = query
        self.website_dir = website_dir
        self.url = url
        self.title = title
        self.synopsis = synopsis
        self.text = ''

        self.synopsis_response = ''
        self.contains_AMR = False
        self.text_response = ''

    def set_site_text(self, text):
        self.text = text

    def get_synopsis_response(self, response_text):
        self.synopsis_response = response_text
        self.process_GPT_response('synopsis')

    def get_GPT_response(self,response_text):
        self.text_response = response_text
        self.process_GPT_response('text')

    def process_GPT_response(self, mode): #TODO
        #   process the text
        if mode == 'synopsis':
            self.contains_AMR = False if self.synopsis_response.lower().strip() != 'yes' else True
        else:
            text = self.text_response[:5].lower().strip()
            if 'yes' in text:
                self.contains_AMR = True
                self.outbreak_dates = 'TODO'
                self.locations = 'TODO'
                self.amr_type = 'TODO'
                self.number_of_people = 'TODO'

            else:
                self.contains_AMR = False
                self.outbreak_dates = ''
                self.locations = ''
                self.amr_type = ''
                self.number_of_people = ''

    def display(self, display_length_max):
            # print("Values of the attributes:")
            for key, value in vars(self).items():
                if type(value) == str:
                    print(f"{key}: {value[:min(len(value),display_length_max)]}")
            print()

def get_chrome_driver():
    # Set ChromeDriver options
    options = webdriver.ChromeOptions()
    # Add any additional options as needed

    # Create ChromeDriver service
    service = Service(ChromeDriverManager().install())

    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    return driver

def get_blacklist():
    banned = []
    with open(os.path.join('tool','website_data','blacklist.txt'),'r') as file:
        banned = file.readlines()
    for i in range(len(banned)):
        banned[i] = banned[i].strip().lower()
    return banned

def check_banned(banned_list, url):
    for i in banned_list:
        if i in url:
            return True
    return False

def check_not_relevant(article_text : str):
    for text in TEXT_TO_AVOID:
        if text in article_text.lower():
            return True
    return False

def scrape_google(queries, start_date=None, end_date=None, num_urls = 9, num_pages = 1):
    driver = get_chrome_driver()
    banned = get_blacklist()

    all_results = []
    for query in queries:
        print(f"Scraping search results for query: {query}")

        if start_date and end_date:
            query += f" after:{start_date} before:{end_date}"
        driver.get('https://www.google.com')

        # Find the search box and input the query
        search_box = driver.find_element(By.NAME, 'q')
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(LARGE_TIME_DELAY)

        # Find all the search result elements
        search_results = driver.find_elements(By.XPATH,'//div[@class="MjjYud"]')
        if len(search_results) == 0:
            time.sleep(SMALL_TIME_DELAY)
            search_results = driver.find_elements(By.XPATH, '//div[@class="TzHB6b cLjAic K7khPe"]')

        # Extract links from search results
        result_objects = []
        searchlimit = num_urls
        for i, result in enumerate(search_results):
            #   stopping when the limit is reached
            if i >= searchlimit:
                break
            #   checking the page isn't the google suggestion box
            if check_not_relevant(result.text.lower()):
                searchlimit += 1
                continue

            try:
                web_page_front = result.find_element(By.XPATH,'.//a')
                #   Getting metadata and the url
                url = web_page_front.get_attribute('href')
                if check_banned(banned,url):
                    searchlimit += 1
                    continue

                title = web_page_front.find_element(By.XPATH,"./h3").text
                website_dir = web_page_front.find_element(By.XPATH, './/div[@class = "byrV5b"]').text
                synopsis = result.find_element(By.XPATH, './/div[@data-snf="nke7rc"]').text
                #   Storing in result object
                cool_little_thing = search_result(query, website_dir, url, title, synopsis)

                if type(cool_little_thing.website_dir) == str or type(cool_little_thing.url) == str:
                    result_objects.append(cool_little_thing)
            except Exception as e:
                print(f"An error occurred while extracting links: {e}")
            #   if the object has data, store it

    
        all_results.extend(result_objects)

        time.sleep(SMALL_TIME_DELAY)  # Delay to prevent hitting Google's rate limits

    driver.quit()

    return all_results

def scrape_sites(search_result_objects):
    driver = get_chrome_driver()
    for search_result in search_result_objects:
        try:
            #   accessing webpage
            driver.get(search_result.url)
            time.sleep(SMALL_TIME_DELAY)
            #   getting capturing and storing text
            p_selectors = driver.find_elements(By.XPATH, '//body//p')
            l_selectors = driver.find_elements(By.XPATH, '//body//ol | //body//ul')
            text = '\n'.join([item.text for item in p_selectors + l_selectors ])
            search_result.set_site_text(text)
        except Exception as e:
            print(f"An error occurred while extracting text: {e}")
    
    driver.quit()


# class ConfigReader:
#     def __init__(self, file_path):
#         self.variables = {}
#         self.read_config(file_path)

#     def read_config(self, file_path):
#         try:
#             with open(file_path, "r") as file:
#                 for line in file:
#                     key = line.strip()
#                     self.variables[key] = None
#         except FileNotFoundError:
#             print(f"Error: File '{file_path}' not found.")

#     def get_variables(self):
#         return self.variables


# class ObjectWithVariables:
#     def __init__(self, variable_list):
#         self.create_variables(variable_list)

#     def create_variables(self, variable_list):
#         for variable in variable_list:
#             setattr(self, variable, None)


# # Example usage:
# file_path = "tools/keywords/variables.txt"  # Adjust the file path accordingly
# config_reader = ConfigReader(file_path)
# variable_list = list(config_reader.get_variables().keys())

# obj = ObjectWithVariables(variable_list)

# # Example of accessing the dynamically created variables
# print(obj.__dict__)
