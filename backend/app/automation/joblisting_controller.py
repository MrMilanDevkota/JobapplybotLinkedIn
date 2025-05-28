import time
import random
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.automation.resume_manager import load_resume_data
from app.automation.application_process_controller import handle_application_process

class JobListingController:
    def process_job_listings(driver, llm, max_applications):
        """Process through the list of jobs and apply to them"""
        print("Processing job listings...")
        applied_count = 0
        jobs_viewed = 0
        applied_jobs = []
        
        # Load resume data for application responses
        resume_data = load_resume_data()
        if not resume_data:
            print("Failed to load resume data, cannot proceed with applications")
            return False
        
        try:
            # Wait for the job list to load with improved selector
            print("Waiting for job listings to load...")
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search-results-list, .scaffold-layout__list"))
            )
            time.sleep(3)  # Additional wait to ensure full loading
            
            print("Identifying job cards...")
            # Try multiple selectors for job cards
            job_cards = []
            for selector in [
                ".job-card-container",
                ".jobs-search-results__list-item",
                "li.jobs-search-results__list-item",
                ".artdeco-list__item"
            ]:
                job_cards = driver.find_elements(By.CSS_SELECTOR, selector)
                if job_cards:
                    print(f"Found {len(job_cards)} job cards using selector: {selector}")
                    break
            
            if not job_cards:
                print("No job cards found. Attempting alternative approach...")
                # Try to get all job cards by their parent container
                containers = driver.find_elements(By.CSS_SELECTOR, ".jobs-search-results-list")
                if containers:
                    print("Found jobs container, looking for cards within it...")
                    job_cards = containers[0].find_elements(By.XPATH, "./div")
                    print(f"Found {len(job_cards)} job cards using container approach")
            
            if not job_cards:
                print("Could not locate job cards. Please check LinkedIn's layout or try another search.")
                return False
            
            # Process job cards
            while applied_count < max_applications and jobs_viewed < len(job_cards):
                try:
                    # Close any open modals before proceeding
                    try:
                        close_buttons = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Dismiss']")
                        for button in close_buttons:
                            if button.is_displayed():
                                driver.execute_script("arguments[0].click();", button)
                                time.sleep(1)
                    except:
                        pass
                    
                    # Get the current job card
                    current_job = job_cards[jobs_viewed]
                    jobs_viewed += 1
                    
                    print(f"Processing job {jobs_viewed}/{len(job_cards)}...")
                    
                    # Scroll the job card into view
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", current_job)
                    time.sleep(1)
                    
                    # Click on the job card with retry mechanism
                    job_clicked = False
                    attempts = 0
                    while not job_clicked and attempts < 3:
                        try:
                            driver.execute_script("arguments[0].click();", current_job)
                            job_clicked = True
                        except:
                            try:
                                # Alternative click method
                                action = webdriver.ActionChains(driver)
                                action.move_to_element(current_job).click().perform()
                                job_clicked = True
                            except:
                                attempts += 1
                                time.sleep(1)
                    
                    if not job_clicked:
                        print("Failed to click job card, skipping to next job")
                        continue
                    
                    # Wait for job details to load
                    time.sleep(2)
                    
                    # Get job details
                    try:
                        job_title_element = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-unified-top-card__job-title, .job-details-jobs-unified-top-card__job-title"))
                        )
                        job_title = job_title_element.text.strip()
                        
                        company_element = driver.find_element(By.CSS_SELECTOR, ".jobs-unified-top-card__company-name, .job-details-jobs-unified-top-card__company-name")
                        company = company_element.text.strip()
                        
                        print(f"Viewing: {job_title} at {company}")
                    except:
                        print("Could not extract job details, but continuing anyway")
                        job_title = "Unknown Position"
                        company = "Unknown Company"
                    
                    # Check for Easy Apply button with comprehensive selectors
                    easy_apply_found = False
                    for selector in [
                        ".jobs-apply-button",
                        "button[aria-label='Easy Apply']",
                        "button.jobs-apply-button",
                        ".jobs-apply-button--top-card",
                        "button[data-control-name='jobdetails_topcard_inapply']"
                    ]:
                        try:
                            easy_apply_button = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                            )
                            print(f"Found Easy Apply button using selector: {selector}")
                            easy_apply_found = True
                            break
                        except:
                            continue
                    
                    if not easy_apply_found:
                        print("No Easy Apply button found for this job, skipping")
                        continue
                    
                    # Click Easy Apply button
                    try:
                        # Scroll to ensure button is in view
                        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", easy_apply_button)
                        time.sleep(1)
                        
                        # Try clicking
                        driver.execute_script("arguments[0].click();", easy_apply_button)
                        time.sleep(2)
                        
                        # Handle the application process
                        if handle_application_process(driver, llm, resume_data, job_title, company):
                            applied_count += 1
                            applied_jobs.append({"company": company, "title": job_title})
                            print(f"Successfully applied to: {job_title} at {company}")
                            print(f"Application {applied_count}/{max_applications} completed")
                            
                            # Add random delay between applications
                            delay = random.uniform(5, 10)
                            print(f"Waiting {delay:.1f} seconds before next application...")
                            time.sleep(delay)
                        else:
                            print(f"Failed to complete application for: {job_title} at {company}")
                            
                            # Try to close any open dialogs
                            try:
                                close_buttons = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Dismiss'], button[aria-label='Close']")
                                for button in close_buttons:
                                    if button.is_displayed():
                                        driver.execute_script("arguments[0].click();", button)
                                        time.sleep(1)
                            except:
                                pass
                    except Exception as e:
                        print(f"Error clicking Easy Apply button: {e}")
                        continue
                    
                    # Check if we've reached our application limit
                    if applied_count >= max_applications:
                        print(f"Reached maximum applications limit ({max_applications})")
                        break
                    
                except Exception as e:
                    print(f"Error processing job card: {e}")
                    continue
                
                # After processing each job, check if more job cards are available
                if jobs_viewed >= len(job_cards) and applied_count < max_applications:
                    print("Looking for more job cards...")
                    
                    # Scroll down to load more jobs
                    job_list_container = driver.find_element(By.CSS_SELECTOR, ".jobs-search-results-list, .scaffold-layout__list")
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", job_list_container)
                    time.sleep(3)
                    
                    # Get updated job cards
                    old_count = len(job_cards)
                    for selector in [
                        ".job-card-container",
                        ".jobs-search-results__list-item",
                        "li.jobs-search-results__list-item",
                        ".artdeco-list__item"
                    ]:
                        job_cards = driver.find_elements(By.CSS_SELECTOR, selector)
                        if len(job_cards) > old_count:
                            print(f"Found {len(job_cards) - old_count} additional job cards")
                            break
                    
                    if len(job_cards) <= old_count:
                        print("No more job cards found. Ending job search.")
                        break
            
            print(f"Application process completed. Applied to {applied_count} jobs.")
            
            # Save the list of jobs we applied to
            with open("applied_jobs.json", "w") as file:
                json.dump(applied_jobs, file, indent=4)
                
            return True
            
        except Exception as e:
            print(f"Error processing job listings: {e}")
            return False