from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

def google_search(query, num_results=10):
    # Path to your ChromeDriver executable
    chromedriver_path = '/path/to/chromedriver'

    # Initialize Chrome WebDriver with the path to chromedriver
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)

    # Go to Google
    driver.get('https://www.google.com')

    # Find the search box and input the query
    search_box = driver.find_element_by_name('q')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    # Find all the search result elements
    search_results = driver.find_elements_by_css_selector('div.g')

    # Extract links from search results
    links = []
    for result in search_results[:num_results]:
        try:
            link = result.find_element_by_css_selector('a').get_attribute('href')
            links.append(link)
        except:
            pass

    # Close the WebDriver
    driver.quit()

    return links

# Example usage
search_query = "web scraping with selenium"
search_results = google_search(search_query)
for i, link in enumerate(search_results, start=1):
    print(f"{i}. {link}")
