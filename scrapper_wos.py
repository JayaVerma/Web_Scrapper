from selenium import webdriver
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
NUM_ARTICLES = 10  # Number of articles to scrape

# Set up the WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Open in full-screen mode
driver = webdriver.Chrome(options=options)

try:
    # 1️⃣ Open the Web of Science Login Page
    driver.get("https://access.clarivate.com/login?app=wos")
    wait = WebDriverWait(driver, 10)

    # 2️⃣ Enter Credentials
    username_input = wait.until(EC.presence_of_element_located((By.ID, "mat-input-0")))
    password_input = driver.find_element(By.ID, "mat-input-1")

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)  # Press Enter to log in

    # 3️⃣ Wait for Login to Complete
    time.sleep(5)  # Adjust based on network speed

    # 4️⃣ Handle the Cookie Popup (if present)
    try:
        accept_cookies = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]")))
        accept_cookies.click()
        print(" Cookies accepted")
    except:
        print("⚠️ No cookie popup found, proceeding...")

    # 5️⃣ Navigate to Web of Science Search Page
    driver.get("https://www.webofscience.com/wos/woscc/basic-search")
    time.sleep(3)  # Allow page to load

    # 6️⃣ Locate the Search Input Field
    search_box = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div.search-criteria-input-holder input.mat-input-element")
    ))

    # 7️⃣ Enter the Search Term and Submit
    search_box.send_keys(SEARCH_TERM)
    search_box.send_keys(Keys.RETURN)

    print(f" Search term '{SEARCH_TERM}' entered successfully!")

#     # Store search results page URL
#     search_results_url = driver.current_url  

#     # Ensure the folder exists
#     if not os.path.exists("wos_scraper"):
#         os.makedirs("wos_scraper")

#     # Extracting article details and downloading pages
#     articles_data = []

#     for i in range(NUM_ARTICLES):
#         print(f" Processing article {i+1}/{NUM_ARTICLES}...")

#         # Refresh search results page before extracting a new article
#         driver.get(search_results_url)
#         time.sleep(5)  # Allow page to reload
        
#         # Re-locate article elements again
#         articles = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".title-link")))

#         if i >= len(articles):  
#             print(f"⚠️ Only {len(articles)} articles found, stopping early.")
#             break  

#         article = articles[i]  
#         title = article.text.strip()
#         link = article.get_attribute("href")

#         if not title or not link:
#             print(f"⚠️ Skipping article {i+1} due to missing data.")
#             continue

#         print(f"🔹 Found: {title} - {link}")

#         # Open article page
#         driver.get(link)
#         time.sleep(5)  # Wait for article page to load

#         # Save the article HTML
#         filename = f"wos_scraper/article_{i+1}.html"
#         html_content = driver.page_source

#         with open(filename, "w", encoding="utf-8") as file:
#             file.write(html_content)

#         print(f" Saved: {filename}")

#         # Store data
#         # articles_data.append({
#         #     "title": article_title,
#         #     "author": author,
#         #     "doi": doi,
#         #     "article_link": article_link,
#         #     "file": filename
#         # })

#         # Go back to search results page
#         driver.get(search_results_url)
#         time.sleep(3)  # Allow page to reload

#     # Save extracted data as JSON
#     json_filename = "wos_scraper/articles_data.json"
#     with open(json_filename, "w", encoding="utf-8") as json_file:
#         json.dump(articles_data, json_file, indent=4)

#     print(f"✅ Successfully saved {len(articles_data)} articles. Data saved in {json_filename}")

except Exception as e:
   print(f"❌ Error: {e}")

# finally:
#     driver.quit()