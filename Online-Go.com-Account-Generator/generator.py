import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Registration details
REGISTER_URL = "https://online-go.com/register"
GROUP_URL = "https://online-go.com/group/12594"
LADDER_URL = "https://online-go.com/ladder/37768"
TOURNAMENT_URL = "https://online-go.com/tournament/118199"

# Account details
EMAIL_SUFFIX = "@example.com"
PASSWORD = "142857"

# Directory to store current account number file
ACCOUNTS_DIRECTORY = r"C:\Users\chang\OneDrive\Desktop\ogs account creator"
ACCOUNT_FILE = os.path.join(ACCOUNTS_DIRECTORY, "current_account.txt")

# Function to read the last account number
def read_last_account_number():
    try:
        with open(ACCOUNT_FILE, "r") as f:
            last_account_number = int(f.read().strip())
    except FileNotFoundError:
        last_account_number = 1  # Start from the beginning if file not found
    return last_account_number

# Function to save the current account number
def save_current_account_number(account_number):
    with open(ACCOUNT_FILE, "w") as f:
        f.write(str(account_number))

# Function to generate random usernames starting with "Auto_" and followed by a random 5-letter string
def generate_random_username(length=5):
    prefix = "Auto_"
    letters = string.ascii_lowercase
    while True:
        random_suffix = ''.join(random.choice(letters) for _ in range(length))
        username = prefix + random_suffix
        return username

# Function to register and join Doulet Media group and ladder for a single account
def register_and_join_account(account_number):
    username = generate_random_username()  # Generate random username with "Auto_" prefix
    email = f"{username.lower()}{EMAIL_SUFFIX}"

    driver = webdriver.Edge()  # Initialize Edge WebDriver

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
        WebDriverWait(driver, 10).until(EC.url_contains(REGISTER_URL))  # Wait until URL changes to indicate successful registration
        print(f"Account {username} registered.")

        time.sleep(2)  # Short delay after registration

        # Choose level (assuming this is done after registration)
        try:
            choose_level_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Overview-Container"]/div[2]/div/div[2]/div[4]/button/span[1]')))
            choose_level_button.click()
            print(f"Chose level for account {username}.")
        except Exception as e:
            print(f"Error choosing level: {str(e)}")

        time.sleep(2)  # Short delay after choosing level

        # After choosing level, navigate to group
        driver.get(GROUP_URL)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="default-variant-container"]/div[2]/div/div[1]/div[1]/div[1]/div[2]/button')))

        join_button = driver.find_element(By.XPATH, '//*[@id="default-variant-container"]/div[2]/div/div[1]/div[1]/div[1]/div[2]/button')
        join_button.click()

        time.sleep(5)  # Longer delay after joining group

        # Navigate to ladder page
        driver.get(LADDER_URL)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="default-variant-container"]/div[2]/div/div[1]/span[2]/button')))

        # Click the button on the ladder page
        ladder_button = driver.find_element(By.XPATH, '//*[@id="default-variant-container"]/div[2]/div/div[1]/span[2]/button')
        ladder_button.click()
        print(f"Clicked the button on the ladder page for account {username}.")

        time.sleep(5)  # Longer delay after joining ladder

        # Navigate to tournament page
        driver.get(TOURNAMENT_URL)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="default-variant-container"]/div[2]/div[3]/div[1]/p/button')))

        # Click the button on the tournament page
        tournament_button = driver.find_element(By.XPATH, '//*[@id="default-variant-container"]/div[2]/div[3]/div[1]/p/button')
        tournament_button.click()
        print(f"Clicked the button on the tournament page for account {username}.")

        # Save the current account number to file after successful account creation
        save_current_account_number(account_number)

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        driver.quit()

# Function to create accounts and join Doulet Media group and ladder within a range using concurrent execution
def create_and_join_accounts(start_account, end_account):
    last_account_number = read_last_account_number()
    account_range = range(last_account_number, end_account + 1)

    with ThreadPoolExecutor(max_workers=8) as executor:  # Adjust max_workers as needed
        futures = [executor.submit(register_and_join_account, account_number) for account_number in account_range]
        for future in as_completed(futures):
            try:
                future.result()  # Ensure all tasks complete without errors
            except Exception as e:
                print(f"Exception occurred: {e}")

    print(f"Finished generating accounts from {start_account} to {end_account}.")
    input("Press Enter to quit.")

# Define the range of accounts to generate
start_account = 1
end_account = 5000  # Adjust as needed

# Execute the function with the specified range of accounts
create_and_join_accounts(start_account, end_account)
