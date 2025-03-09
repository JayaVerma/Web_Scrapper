from selenium import webdriver
import time

# Set up the WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Open in full-screen mode
driver = webdriver.Chrome(options=options)

website = "https://www.webofscience.com/wos/woscc/basic-search"


driver.get(website)
time.sleep(5)


driver.quit()