from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
    wait = WebDriverWait(driver, 15)

    # 2️⃣ Enter Credentials
    username_input = wait.until(EC.presence_of_element_located((By.ID, "mat-input-0")))
    password_input = driver.find_element(By.ID, "mat-input-1")

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)  # Press Enter to log in

    # 3️⃣ Wait for Login to Complete
    time.sleep(7)  # Adjust based on network speed

    # 4️⃣ Handle the Cookie Popup (if present)
    try:
        accept_cookies = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]")))
        accept_cookies.click()
        print("✅ Cookies accepted")
    except:
        print("⚠️ No cookie popup found, proceeding...")

    # 5️⃣ Navigate to Web of Science Search Page
    driver.get("https://www.webofscience.com/wos/woscc/basic-search")
    time.sleep(5)  # Allow page to load

    # 6️⃣ Locate the Search Input Field
    search_box = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div.search-criteria-input-holder input.mat-input-element")
    ))

    # 7️⃣ Enter the Search Term and Submit
    search_box.send_keys(SEARCH_TERM)
    search_box.send_keys(Keys.RETURN)

    print(f"✅ Search term '{SEARCH_TERM}' entered successfully!")

    # 8️⃣ Wait for results to load
    time.sleep(20)

    # 9️⃣ Extract article titles and URLs
    articles = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "app-record")))

    for article in articles:
        try:
            title_element = article.find_element(By.CSS_SELECTOR, "a[data-ta='summary-record-title-link']")
            title = title_element.text.strip()
            link = title_element.get_attribute("href")
            print(f"Title: {title}\nURL: {link}\n")
        except Exception as e:
            print(f"⚠️ Could not extract article: {e}")

finally:
    # 1️⃣0️⃣ Close the WebDriver
    driver.quit()
