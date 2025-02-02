import traceback
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def wait_for_page_load(driver):
    """Wait until the page is fully loaded (wait for body to be visible)."""
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.TAG_NAME, "body"))
    )

def wait_for_log_load(driver):
    """Wait until the page is fully loaded (wait for an element with class 'css-r6sydd no-touch. It isnt working as well.')."""
    WebDriverWait(driver, 80).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "css-r6sydd"))
    )

def wait_for_rewards_points(driver):
    """Wait until the rewards points element is visible."""
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'css-1d2mlvq') and contains(@class, 'e15t7owz0')]"))
    )

def main():
    # Set up Chrome options
    options = Options()
    options.add_argument("--incognito")

    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.geolocation": 2  
    })
    # options.add_argument("--headless")  # Uncomment this line to run in headless mode

    # Set up Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://www.sephora.com/")  # Open the Sephora website

    # Wait for the page to fully load (ensuring all JavaScript finishes)
    print("Waiting for page to load completely...")
    wait_for_page_load(driver)
    print("Page is fully loaded.")

    # Optionally, set window size for proper rendering
    driver.set_window_size(1920, 1080)  # Full HD resolution

    try:
        # Check if the element is present in the DOM first
        print("Checking for the 'Sign In for Free Shipping' button in DOM...")
        sign_in_button = driver.find_element(By.ID, "account_drop_trigger")
        print("Element found in DOM:", sign_in_button)

        # Wait for the login form to appear (username and password fields)
        print("Waiting for the username field to be visible...")
        username_field = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, "signin_username"))
        )
        print("Username field visible.")

        # Enter username
        username_field.send_keys("email@gmail.com")
        print("Username entered.")

        # Wait for the password field to appear
        print("Waiting for password field to be visible...")
        password_field = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        )
        print("Password field visible. Yeah baby")

        # Enter password
        password_field.send_keys("your_password")
        print("Password entered.")

        # Submit the login form by pressing Enter
        password_field.send_keys(Keys.RETURN)
        print("Login form submitted.")

        # Wait for the new page to load
        wait_for_log_load(driver)

        # Wait a bit to ensure the page has loaded
        print("Login Worked sucker! New page loaded successfully.")

        # Save the page source for inspection
        page_source = driver.page_source
        with open("page_source_after_login.html", "w") as file:
            file.write(page_source)
        print("Page source saved to 'page_source_after_login.html'. Please inspect it for the rewards points element.")

        # Parse the page source with BeautifulSoup for debugging
        soup = BeautifulSoup(page_source, 'html.parser')
        rewards_points_debug = soup.find("div", class_="css-1d2mlvq e15t7owz0")

        if rewards_points_debug:
            print("Rewards points found in the HTML source:", rewards_points_debug)
        else:
            print("Could not find the rewards points element in the page source.")
	
	# The issue starts here!
        # Wait for the rewards points element to become visible
        print("Waiting for the rewards points element to load...")
        wait_for_rewards_points(driver)

        # Get the rewards points element after waiting for it to be visible
        points_element = driver.find_element(By.XPATH, "//div[contains(@class, 'css-1d2mlvq') and contains(@class, 'e15t7owz0')]")
        rewards_points = points_element.find_element(By.TAG_NAME, "strong").text.strip()
        print(f"Your rewards points: {rewards_points}")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        with open("error_page_source.html", "w") as file:
            file.write(driver.page_source)  # Save page source for debugging
        print("Page source saved for debugging.")

    finally:
        driver.quit()
        print("Browser session ended.")

if __name__ == "__main__":
    main()
