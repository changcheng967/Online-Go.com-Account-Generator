from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Registration details
BASE_URL = "https://online-go.com"
REGISTER_URL = BASE_URL + "/register"
GROUP_URL = BASE_URL + "/group/12594"

# Account details
EMAIL_SUFFIX = "@example.com"
PASSWORD = "142857"

# Function to create accounts and join Doulet Media group
def create_and_join_accounts():
    i = 1
    while True:
        username = f"fanofdouletmedia{i}"
        email = f"{username.lower()}{EMAIL_SUFFIX}"

        driver = webdriver.Chrome()  # Change this to your WebDriver (e.g., Edge, Firefox)

        try:
            # Register account
            driver.get(REGISTER_URL)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

            username_input = driver.find_element(By.ID, "username")
            username_input.clear()
            username_input.send_keys(username)

            password_input = driver.find_element(By.ID, "password")
            password_input.clear()
            password_input.send_keys(PASSWORD)

            email_input = driver.find_element(By.ID, "email")
            email_input.clear()
            email_input.send_keys(email)

            # Submit registration
            register_button = driver.find_element(By.XPATH, '//*[@id="Register"]/div/div[1]/form/div/button')
            register_button.click()

            # Wait for registration to complete
            WebDriverWait(driver, 10).until(EC.url_contains(BASE_URL))  # Wait until URL changes to indicate successful registration
            print(f"Account {username} registered.")

            time.sleep(2)  # Short delay after registration

            # After registration, navigate to group
            driver.get(GROUP_URL)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="default-variant-container"]/div[2]/div/div[1]/div[1]/div[1]/div[2]/button')))

            join_button = driver.find_element(By.XPATH, '//*[@id="default-variant-container"]/div[2]/div/div[1]/div[1]/div[1]/div[2]/button')
            join_button.click()

            # Wait for join confirmation
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.group-join-success'), 'You are now a member of this group.'))
            print(f"Account {username} joined Doulet Media group.")

        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            driver.quit()

        # Increment username number for the next account
        i += 1
        time.sleep(1)  # Short delay before generating the next account

# Execute the function
create_and_join_accounts()
