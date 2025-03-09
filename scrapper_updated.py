from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import os

# User-provided inputs
USERNAME = "username@usf.edu"
PASSWORD = "password!"
SEARCH_TERM = "Polymer Protein"
NUM_ARTICLES = 50  # Get all articles from the first page

# Set up WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    # 1️⃣ Open Web of Science Login Page
    driver.get("https://access.clarivate.com/login?app=wos")
    wait = WebDriverWait(driver, 15)

    # 2️⃣ Enter Credentials
    username_input = wait.until(EC.presence_of_element_located((By.ID, "mat-input-0")))
    password_input = driver.find_element(By.ID, "mat-input-1")

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)

    # 3️⃣ Wait for Login to Complete
    time.sleep(5)

    # 4️⃣ Handle Cookie Popup (if any)
    try:
        accept_cookies = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]")))
        accept_cookies.click()
        print("✅ Cookies accepted")
    except:
        print("⚠️ No cookie popup found, proceeding...")

    # 5️⃣ Navigate to Web of Science Search Page
    driver.get("https://www.webofscience.com/wos/woscc/basic-search")
    time.sleep(3)

    # 6️⃣ Enter the Search Term and Submit
    search_box = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div.search-criteria-input-holder input.mat-input-element")
    ))
    search_box.send_keys(SEARCH_TERM)
    search_box.send_keys(Keys.RETURN)
    print(f"✅ Search term '{SEARCH_TERM}' entered successfully!")

    # 7️⃣ Scrape Journal Articles
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.find_all('app-record', class_='app-record-holder new-link-style ng-star-inserted Summary-record-view')
    
    journal_data = []
    for article in articles[:NUM_ARTICLES]:
        title_tag = article.find('app-summary-title').find('h3')
        link_tag = article.find('a', class_='summary-record-title-link')
        
        title = title_tag.text.strip() if title_tag else 'No Title Found'
        link = link_tag['href'] if link_tag else 'No Link Found'
        
        journal_data.append({'Title': title, 'Link': link})
    
    # Print extracted journal data
    for entry in journal_data:
        print(f"Title: {entry['Title']}")
        print(f"Link: {entry['Link']}")
        print("-" * 40)
    
finally:
    driver.quit()  # Close the browser session
