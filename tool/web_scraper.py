from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import os

TEXT_TO_AVOID = ['scholarly articles' , 'people also ask', 'local results']
SMALL_TIME_DELAY = 5
LARGE_TIME_DELAY = SMALL_TIME_DELAY * 2

def assign_constants(avoided_text,small_delay, large_delay):
    global TEXT_TO_AVOID, SMALL_TIME_DELAY, LARGE_TIME_DELAY
    TEXT_TO_AVOID, SMALL_TIME_DELAY, LARGE_TIME_DELAY = avoided_text, small_delay, large_delay

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
        self.process_response(response_text)

    def get_GPT_response(self,response_text):
        self.text_response = response_text
        self.process_response(response_text)

    def process_response(self, text):
        if 'yes' in text[:min(50,len(text))].lower():
            self.contains_AMR = True
        else:
            self.contains_AMR = False

    def set_variable(self,variable_name, variable_value):
        setattr(self,variable_name,variable_value)

    def display(self, display_length_max):
            # print("Values of the attributes:")
            for key, value in vars(self).items():
                if type(value) == str:
                    print(f"{key}: {value[:min(len(value),display_length_max)]}")
            print()            

def get_chrome_driver():
    # Set ChromeDriver options
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.notifications": 2})  # Disable notifications
    # Add any additional options as needed

    # Create ChromeDriver service
    service = Service(ChromeDriverManager().install())

    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    return driver

# def get_chrome_driver():
#     # Set ChromeDriver options
#     options = webdriver.ChromeOptions()
#     options.add_argument("--disable-notifications")
#     # Add any additional options as needed

#     # Create ChromeDriver service
#     service = Service(ChromeDriverManager().install())

#     # Initialize Chrome WebDriver
#     driver = webdriver.Chrome(service=service, options=options)

#     return driver

def get_blacklist():
    with open(os.path.join('tool','website_data','blacklist.txt'),'r') as file:
        banned = file.readlines()
    for i in range(len(banned)):
        banned[i] = banned[i].strip().lower()
    return banned

def process_scraped_urls(mode : str = 'access', url : str = None):
    if mode == 'access':
        with open(os.path.join('tool','website_data','urls.txt'),'r') as file:
            urls = file.readlines()
        for i in range(len(urls)):
            urls[i] = urls[i].strip().lower()
        return urls
    else:
        with open(os.path.join('tool','website_data','urls.txt'),'a') as file:
            file.write(url + '\n')

def check_not_relevant(article_text : str):
    for text in TEXT_TO_AVOID:
        if text in article_text.lower():
            return True
    return False

def url_excluded(url, blacklisted_sites,seen_urls):
    excluded = False
    for site in blacklisted_sites:
        if site.lower() in url.lower():
            excluded = True
            break
    for seen in seen_urls:
        if seen.lower() in url.lower():
            excluded = True
            break
    return excluded

def scrape_google(queries, start_date=None, end_date=None, max_time = 5, num_results = 5, news = True):
    driver = get_chrome_driver()
    banned_urls = get_blacklist()
    seen_urls = process_scraped_urls()

    all_results = []
    for query in queries:
        print(f"Scraping search results for query: {query}")

        if start_date and end_date:
            query += f" after:{start_date} before:{end_date}"
        driver.set_page_load_timeout(max_time)
        
        if not news:
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
            accepted_results = 0
            for result in search_results:
                #   checking the page isn't the google suggestion box
                if check_not_relevant(result.text.lower()):
                    continue

                if accepted_results >= num_results:
                    break

                try:
                    web_page_front = result.find_element(By.XPATH,'.//a')
                    #   Getting metadata and the url
                    url = web_page_front.get_attribute('href')
                    if url_excluded(url,banned_urls,seen_urls):
                        continue
                    title = web_page_front.find_element(By.XPATH,"./h3").text
                    website_dir = web_page_front.find_element(By.XPATH, './/div[@class = "byrV5b"]').text
                    synopsis = result.find_element(By.XPATH, './/div[@data-snf="nke7rc"]').text
                    #   Storing in result object
                    cool_little_thing = search_result(query, website_dir, url, title, synopsis)

                    if type(cool_little_thing.website_dir) == str or type(cool_little_thing.url) == str:
                        process_scraped_urls('add',url)
                        result_objects.append(cool_little_thing)
                        accepted_results += 1
                except Exception as e:
                    print(f"An error occurred while extracting links: {e}")

            all_results.extend(result_objects)

            time.sleep(SMALL_TIME_DELAY)  # Delay to prevent hitting Google's rate limits
        else:
            driver.get('https://www.google.com/news')

            # Find the search box and input the query
            search_box = driver.find_element(By.CSS_SELECTOR,'input')
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            time.sleep(LARGE_TIME_DELAY)

            # Find all the search result elements
            search_results = driver.find_elements(By.XPATH,'//c-wiz[@jsrenderer="ARwRbe"]')
            if len(search_results) == 0:
                time.sleep(SMALL_TIME_DELAY)
                search_results = driver.find_elements(By.XPATH,'//c-wiz[@jsrenderer="ARwRbe"]')

            # Extract links from search results
            result_objects = []
            accepted_results = 0
            for result in search_results:
                #   checking the page isn't the google suggestion box
                if check_not_relevant(result.text.lower()):
                    continue

                if accepted_results >= num_results:
                    break

                try:
                    title = result.find_element(By.XPATH,'.//a').text
                    #   Getting metadata and the url
                    url = web_page_front.get_attribute('href')
                    if url_excluded(url,banned_urls,seen_urls):
                        continue
                    title = web_page_front.find_element(By.XPATH,"./h3").text
                    website_dir = web_page_front.find_element(By.XPATH, './/div[@class = "byrV5b"]').text
                    synopsis = result.find_element(By.XPATH, './/div[@data-snf="nke7rc"]').text
                    #   Storing in result object
                    cool_little_thing = search_result(query, website_dir, url, title, synopsis)

                    if type(cool_little_thing.website_dir) == str or type(cool_little_thing.url) == str:
                        process_scraped_urls('add',url)
                        result_objects.append(cool_little_thing)
                        accepted_results += 1
                except Exception as e:
                    print(f"An error occurred while extracting links: {e}")

            all_results.extend(result_objects)

            time.sleep(SMALL_TIME_DELAY)  # Delay to prevent hitting Google's rate limits
    driver.quit()

    return all_results

def scrape_sites(search_result_objects, max_time):
    driver = get_chrome_driver()
    driver.set_page_load_timeout(max_time)

    for search_result in search_result_objects:
        try:
            #   accessing webpage
            driver.get(search_result.url)
            time.sleep(SMALL_TIME_DELAY)
            #   getting capturing and storing text
            p_selectors = driver.find_elements(By.XPATH, '//body//p')
            l_selectors = driver.find_elements(By.XPATH, '//body//ol | //body//ul')
            text = '\n'.join([item.text for item in p_selectors + l_selectors ])
            if len(text) < 200:
                text = '\n'.join(driver.find_elements(By.XPATH, '//body//div'))
            search_result.set_site_text(text)
        except Exception as e:
            print(f"An error occurred while extracting text: {e}")

    driver.quit()



'''import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

BUSINESS = 'CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=enUS&gl=US&ceid=US%3Aen'
WORLD = 'CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen'

categories = [WORLD, BUSINESS]
random_category = random.choice(categories)

# Navigate to Google News
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(f"https://news.google.com/topics/{random_category}")

wait = WebDriverWait(driver, 10)
a = wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "article > div > a")))
print(f"Title: {a[0].get_attribute('aria-label')}")
original_window = driver.current_window_handle
a[0].click()
wait.until(EC.number_of_windows_to_be(2))
for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break

wait.until(EC.none_of(EC.url_contains("news.google.com")))

print(driver.current_url)'''