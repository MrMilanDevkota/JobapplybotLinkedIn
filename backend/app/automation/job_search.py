import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class JobSearch:
    def navigate_to_jobs_and_search(self, driver, job_title, location):
        # Navigate to LinkedIn Jobs and search using the specific input elements
        try:
            print("Navigating to LinkedIn Jobs page...")
            driver.get("https://www.linkedin.com/jobs/")
            time.sleep(3)  # Give page time to fully load

            # Try to find the job title input field using multiple selectors
            print("Looking for job title input field...")
            job_title_input = None
            try:
                job_title_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']"))
                )
            except:
                try:
                    job_title_input = driver.find_element(By.CSS_SELECTOR, ".jobs-search-box__text-input.jobs-search-box__keyboard-text-input")
                except:
                    try:
                        inputs = driver.find_elements(By.CSS_SELECTOR, "input[id*='jobs-search-box-keyword']")
                        if inputs:
                            job_title_input = inputs[0]
                    except:
                        pass

            if not job_title_input:
                print("Could not find job title input field.")
                return False

            print(f"Entering job title: {job_title}")
            job_title_input.clear()
            time.sleep(1)
            job_title_input.send_keys(job_title)
            time.sleep(1)

            # Find location input field
            print("Looking for location input field...")
            location_input = None
            try:
                location_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[aria-label='City, state, or zip code']"))
                )
            except:
                try:
                    inputs = driver.find_elements(By.CSS_SELECTOR, "input[id*='jobs-search-box-location']")
                    if inputs:
                        location_input = inputs[0]
                except:
                    pass

            if not location_input:
                print("Could not find location input field.")
                return False

            print(f"Entering location: {location}")
            location_input.clear()
            time.sleep(1)
            location_input.send_keys(location)
            time.sleep(1)

            # Press Enter to submit the search
            print("Submitting search...")
            location_input.send_keys(Keys.RETURN)

            # Wait for search results to load
            print("Waiting for search results...")
            time.sleep(5)

            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search-results-list, .jobs-search__job-details"))
                )
                print("Job search completed successfully.")
                return True
            except:
                current_url = driver.current_url
                if "keywords=" in current_url and ("location=" in current_url or "geoId=" in current_url):
                    print("Job search URL detected, search appears successful.")
                    return True
                else:
                    print("Could not confirm if job search was successful.")
                    return False

        except Exception as e:
            print(f"Error during job search: {e}")
            return False

    def click_easy_apply_filter(self, driver):
        """Click the Easy Apply filter button"""
        try:
            print("Looking for Easy Apply filter button...")
            easy_apply_button = None
            for selector in [
                By.ID, "searchFilter_applyWithLinkedin",
                By.CSS_SELECTOR, "button[aria-label='Easy Apply filter.']",
                By.XPATH, "//button[contains(., 'Easy Apply')]", # Use XPATH for text content
                By.CSS_SELECTOR, ".artdeco-pill--choice" # More general CSS
            ]:
                if selector == By.ID:
                    try:
                        easy_apply_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((selector, "searchFilter_applyWithLinkedin"))
                        )
                        break
                    except:
                        pass
                else:
                    try:
                        easy_apply_button = driver.find_element(selector, selector[1])
                        if easy_apply_button.is_displayed() and easy_apply_button.is_enabled():
                            break
                    except:
                        pass


            if not easy_apply_button:
                print("Could not find Easy Apply filter button.")
                return False

            print("Clicking Easy Apply filter button...")
            driver.execute_script("arguments[0].click();", easy_apply_button)
            time.sleep(3)

            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-checked='true'][aria-label='Easy Apply filter.']"))
                )
                print("Easy Apply filter was successfully applied.")
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search-results-list"))
                )
                print("Job listings updated with Easy Apply filter.")
                return True
            except:
                print("Could not confirm if Easy Apply filter was applied.")
                return False

        except Exception as e:
            print(f"Error clicking Easy Apply filter: {e}")
            return False