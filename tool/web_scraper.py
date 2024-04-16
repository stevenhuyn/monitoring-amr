from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from webdriver_manager.chrome import ChromeDriverManager
import time

'''
TODO
Search Object
    Improve assigning
    Add more variables

Scraping
    Implement number of pages 
    Method for scraping google VS specific pages that we want to keep track of

Things to search
    Date                    The date the article was written
    Outbreak Date           The date the outbreak was seen to have started or a date mentioned that concerns the outbreak.
    Human Scale             The number of people affected.
    City Scale              The number of cities affected.
    Region Scale            The number of regions affected.
    Locations               A comma separated list of locations.
    Anti-microbial Use      Were anti-microbials administered.
    Case                    ?? Resistance?? 
    Locations               A comma separated list of locations.

'''
TEXT_TO_AVOID = ['scholarly articles' , 'people also ask', 'local results']
SMALL_TIME_DELAY = 5
LARGE_TIME_DELAY = SMALL_TIME_DELAY * 2

class search_result:
    def __init__(self,query):
        self.query = query
        self.site = ''
        self.link = ''
        self.title = ''
        self.text = ''

        self.contains_AMR = False
        self.GPT_response = ''

    def set_site_info(self,site,link,title):
        self.site, self.link, self.title = site, link, title

    def set_site_text(self, text):
        self.text = text

    def get_GPT_response(self,response_text):
        self.GPT_response = response_text

    def process_GPT_response(self):
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

<<<<<<< Updated upstream
def scrape_google(queries, start_date=None, end_date=None, num_urls = 9, num_pages = 1):
=======
def check_not_relevant(article_text):
    for text in TEXT_TO_AVOID:
        if text in article_text.lower():
            return True
    return False

def scrape_google(queries, num_urls = 9, num_pages = 1):
>>>>>>> Stashed changes
    driver = get_chrome_driver()

    all_results = []
    for query in queries:
        print(f"Scraping search results for query: {query}")

        if start_year and end_year:
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

            #   instantiating result object
            cool_little_thing = search_result(query)

            try:
                web_page_front = result.find_element(By.XPATH,'.//a')
                #   Getting metadata and the url
                link = web_page_front.get_attribute('href')
                title = web_page_front.find_element(By.XPATH,"./h3").text
                site = web_page_front.find_element(By.XPATH, './/div[@class = "byrV5b"]').text
                #   Storing in result object
                cool_little_thing.set_site_info(site, link, title)

            except Exception as e:
                print(f"An error occurred while extracting links: {e}")
            #   if the object has data, store it
            if cool_little_thing.site != '' or cool_little_thing.link != '':
                result_objects.append(cool_little_thing)
    
        all_results.extend(result_objects)

        time.sleep(SMALL_TIME_DELAY)  # Delay to prevent hitting Google's rate limits

    driver.quit()

    return all_results

def scrape_sites(search_result_objects):
    driver = get_chrome_driver()
    for search_result in search_result_objects:
        try:
            #   accessing webpage
            driver.get(search_result.link)
            time.sleep(SMALL_TIME_DELAY)
            #   getting capturing and storing text
            p_selectors = driver.find_elements(By.XPATH, '//body//p')
            l_selectors = driver.find_elements(By.XPATH, '//body//ol | //body//ul')
            text = '\n'.join([item.text for item in p_selectors + l_selectors ])
            search_result.set_site_text(text)
        except Exception as e:
            print(f"An error occurred while extracting text: {e}")
    
    driver.quit()
