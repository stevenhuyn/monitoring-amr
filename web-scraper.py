from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Import Keys module
from webdriver_manager.chrome import ChromeDriverManager
import time

class search_result:
    def __init__(self):
        self.site = None
        self.link = None
        self.title = None

    def assign(self,site = None, link = None, title = None):
        if site != None:
            self.site = site
        if link != None:
            self.link = link
        if title != None:
            self.title = title

    def display(self):
            print("Values of the attributes:")
            for key, value in vars(self).items():
                print(f"{key}: {value}")
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

def scrape_google_search_results(queries, num_results=10):
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
        
        # Extract links from search results
        result_objects = []
        tempvar = num_results
        for result in search_results[:tempvar]:
            if "people also ask" in result.text.lower():
                tempvar += 1
                continue

            cool_little_thing = search_result()

            try:
                link = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                cool_little_thing.assign(link=link)

                site = result.find_element(By.CSS_SELECTOR,'a')
                h3 = site.find_element(By.XPATH,"./h3")
                title = h3.text
                cool_little_thing.assign(title = title)
            
                site = site.find_element(By.XPATH,"./div/div/div/div/span").text
                cool_little_thing.assign(site=site)

            except Exception as e:
                print(f"An error occurred while extracting links: {e}")
            result_objects.append(cool_little_thing)

        all_results.extend(result_objects)

        time.sleep(2)  # Adding a delay to prevent hitting Google's rate limits

    driver.quit()

    return all_results

# Example usage
queries = ["machine learning"]
search_results = scrape_google_search_results(queries, num_results=10)
print("Search Results:")
for i, result in enumerate(search_results):
    print(f"Result {i+1}")
    result.display()
