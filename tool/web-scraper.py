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
    Filter items by date
    Don't scrape everything - scrape only certain tags
    Investiage reader mode
    Implement number of pages / number of urls
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

class search_result:
    def __init__(self):
        self.site = None
        self.link = None
        self.title = None
        self.text = None

    def assign(self,site = None, link = None, title = None, text = None):
        if site != None:
            self.site = site
        if link != None:
            self.link = link
        if title != None:
            self.title = title
        if text != None:
            self.text = text

    def display(self, display_length_max):
            # print("Values of the attributes:")
            for key, value in vars(self).items():
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

def output_to_csv(scraped_data):
    pass

def scrape_google(queries, num_urls = 9, num_pages = 1):
    driver = get_chrome_driver()

    all_results = []
    for query in queries:
        print(f"Scraping search results for query: {query}")
        driver.get('https://www.google.com')

        # Find the search box and input the query
        search_box = driver.find_element(By.NAME, 'q')
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Find all the search result elements
        search_results = driver.find_elements(By.CLASS_NAME, 'ULSxyf') + driver.find_elements(By.CLASS_NAME, 'MjjYud')

        if len(search_results) < 3:
            search_results = driver.find_elements(By.XPATH,"//body[@id='gsr']//*[contains(@class, 'TzHB6b cLjAic K7khPe')]")
            print("made it this far",len(search_results))
        
        # Extract links from search results
        result_objects = []
        tempvar = min(len(search_results),num_urls)
        for result in search_results[:tempvar]:
            if "people also ask" in result.text.lower():
                tempvar += 1 if tempvar < len(search_results) - 1 else 0
                continue

            cool_little_thing = search_result()

            try:
                web_page_front = result.find_element(By.CSS_SELECTOR,'a')

                link = web_page_front.get_attribute('href')
                title = web_page_front.find_element(By.XPATH,"./h3").text

                site = web_page_front.find_element(By.XPATH,"./div/div/div/div/span").text #TODO Make better with xpath
                
                cool_little_thing.assign(site, link, title)
            except Exception as e:
                print(f"An error occurred while extracting links: {e}")
            
            if cool_little_thing.site != None or cool_little_thing.link != None:
                result_objects.append(cool_little_thing)

        all_results.extend(result_objects)

        time.sleep(2)  # Delay to prevent hitting Google's rate limits

    driver.quit()

    return all_results

def expand_results(search_result_objects):
    driver = get_chrome_driver()
    for search_result in search_result_objects:
        driver.get(search_result.link)

        try:
            page_body = driver.find_element(By.CSS_SELECTOR, 'body')

            search_result.assign(text = page_body.text)
        except Exception as e:
            print(f"An error occurred while extracting text: {e}")
        
        time.sleep(2) # Delay to prevent hitting Google's rate limits
    
    driver.quit()

queries = ["machine learning"]
number_of_pages_to_scrape = 1 #TODO, still need to implement
number_of_urls_per_page = 3
maximum_text_display_length = 500

search_results = scrape_google(queries, num_urls= number_of_urls_per_page, 
        num_pages = number_of_pages_to_scrape)  #   Gets websites and urls from specified pages of google
expand_results(search_results)  #   Accesses links and gets text
print("Search Results:")
for i, result in enumerate(search_results):
    print(f"Result {i+1}")
    result.display(maximum_text_display_length)