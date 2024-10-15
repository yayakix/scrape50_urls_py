from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd

# Function to extract URLs from a given page
def extract_urls(driver, url, depth):
    driver.get(url)
    elems = driver.find_elements(By.XPATH, "//a[@href]")
    urls = []
    
    for elem in elems:
        href = elem.get_attribute("href")
        if href and href.startswith("http"):  # Filter out relative URLs
            urls.append((href, depth))
            if len(urls) >= 10:  # Limit to 10 URLs
                break
    
    return urls

# Function to crawl pages
def crawl(start_url, max_depth):
    print('step 1')
    visited = set()  # avoid revisiting URLs
    results = []

    # Create a new instance of the Chrome driver
    chrome_options = Options()
    service = Service() 
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print('step 2')

    def crawl_recursive(url, depth):
        if depth > max_depth or url in visited:
            return
        visited.add(url)
        
        # Extract URLs from the current page
        urls_on_page = extract_urls(driver, url, depth)
        results.extend(urls_on_page)
        
        # Recursively visit each URL found on the current page
        for href, _ in urls_on_page:
            crawl_recursive(href, depth + 1)

    crawl_recursive(start_url, 0)

    # Quit the driver
    driver.quit()
    
    return results

# Start
start_url = 'https://example.com/'

max_depth = int(input("Enter the number of pages to explore (depth): "))

print('Starting crawl')
# Crawl
found_urls = crawl(start_url, max_depth)

# Convert to DataFrame and print results
df = pd.DataFrame(found_urls, columns=["URL", "Depth"])
print(df)
