from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LinkedInLogin:
    def __init__(self):
        #you kura haru user le input garxa form ma 
        # self.LINKEDIN_EMAIL = self.config.LINKEDIN_EMAIL
        # self.LINKEDIN_PASSWORD = self.config.LINKEDIN_PASSWORD
        pass

    def login_with_credentials(self, driver):
        """Login to LinkedIn using credentials from .env file"""
        driver.get("https://www.linkedin.com/login")

        try:
            # Wait for email field and enter email
            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.send_keys(self.LINKEDIN_EMAIL)

            # Enter password
            password_field = driver.find_element(By.ID, "password")
            password_field.send_keys(self.LINKEDIN_PASSWORD)

            # Click login button
            login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()

            # Wait for successful login
            WebDriverWait(driver, 10).until(
                EC.url_contains("linkedin.com/feed")
            )
            print("Successfully logged in with credentials.")
            return True

        except Exception as e:
            print(f"Login failed: {e}")
            return False