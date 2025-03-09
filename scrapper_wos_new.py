import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dotenv import load_dotenv
import os

load_dotenv()

# Setup logging
def setup_logger():
    logging.basicConfig(
        filename="wos_scraper.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

# Initialize WebDriver
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)

# Secure login handling
def login(driver):
    username = os.getenv("WOS_USERNAME")
    password = os.getenv("WOS_PASSWORD")
    if not username or not password:
        logging.error("Missing Web of Science credentials in environment variables.")
        raise ValueError("Please set WOS_USERNAME and WOS_PASSWORD as environment variables.")

    driver.get("https://access.clarivate.com/login?app=wos")
    wait = WebDriverWait(driver, 10)
    try:
        username_input = wait.until(EC.presence_of_element_located((By.ID, "mat-input-0")))
        password_input = driver.find_element(By.ID, "mat-input-1")
        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        
        # Handle CAPTCHA detection
        time.sleep(3)
        if "captcha" in driver.page_source.lower():
            logging.warning("CAPTCHA detected! Manual intervention required.")
            input("Please complete the CAPTCHA in the browser and press Enter to continue...")
        
        # Handle cookies popup
        try:
            accept_cookies = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]")))
            accept_cookies.click()
        except TimeoutException:
            pass
        
        logging.info("Login successful.")
    except Exception as e:
        logging.error(f"Login failed: {e}")
        driver.quit()
        raise

# Perform article search
def search_articles(driver, search_term):
    driver.get("https://www.webofscience.com/wos/woscc/basic-search")
    wait = WebDriverWait(driver, 10)
    try:
        search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-criteria-input-holder input.mat-input-element")))
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
        logging.info(f"Search for '{search_term}' completed.")
    except TimeoutException:
        logging.error("Search box not found!")
        raise

# Extract total pages
def get_total_pages(driver):
    try:
        page_info = driver.find_element(By.CSS_SELECTOR, ".pagination-info").text
        total_pages = int(page_info.split()[-1])
        return total_pages
    except NoSuchElementException:
        return 1

# Scrape article details
def scrape_articles(driver, num_articles):
    results = []
    total_pages = get_total_pages(driver)
    current_page = 1
    wait = WebDriverWait(driver, 10)
    
    while len(results) < num_articles and current_page <= total_pages:
        articles = driver.find_elements(By.CSS_SELECTOR, ".title-link")
        for article in articles:
            title = article.text
            link = article.get_attribute("href")
            results.append((title, link))
            logging.info(f"Found article: {title} - {link}")
            if len(results) >= num_articles:
                break
        
        if len(results) < num_articles:
            try:
                next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".next-button")))
                next_button.click()
                time.sleep(2)
                current_page += 1
            except TimeoutException:
                break
    
    return results

# Save articles to files
def save_articles(driver, results):
    os.makedirs("wos_articles", exist_ok=True)
    for index, (title, link) in enumerate(results):
        driver.get(link)
        time.sleep(3)
        html_content = driver.page_source
        filename = f"wos_articles/article_{index+1}.html"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(html_content)
        logging.info(f"Saved article: {filename}")

# Main execution function
def main():
    setup_logger()
    search_term = "Machine Learning"
    num_articles = 10
    
    driver = init_driver()
    try:
        login(driver)
        search_articles(driver, search_term)
        results = scrape_articles(driver, num_articles)
        save_articles(driver, results)
        logging.info(f"Successfully saved {len(results)} articles.")
    except Exception as e:
        logging.error(f"Execution failed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
