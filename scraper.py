from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib.request
from datetime import date
from db import get_user_credentials
import os

today = date.today()


def get_driver():
    options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.getenv("CHROME_BIN", "/usr/bin/chromium")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    options.add_argument("--headless=new")  # Run without GUI (optional)
    options.add_argument("--window-size==1920,1080")  
    options.add_argument("--start-maximized")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.binary_location = "/usr/bin/chromium"

    return webdriver.Chrome(
            service = Service(os.getenv("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")),
            options=options
        )


url = "https://student.qspiders.com"

# import shutil
# print("chromium path:", shutil.which("chromium"))           # Should print /usr/bin/chromium
# print("chromium-browser path:", shutil.which("chromium-browser"))  # Should print None


# driver.quit()


name_xpath = '/html/body/div/div/section/div[2]/div[1]/div/div/div[1]/div/div/div/div/input'
password_xpath = '/html/body/div/div/section/div[2]/div[1]/div/div/div[2]/div/div/div/div/input'
login_xpath = '//*[@id="app"]/div/section/div[2]/div[2]/div[2]/button'
qr_xpath = '//*[@id="navbarid"]/div[5]/div/div[9]/div'
image_xpath = '//*[@id="navbarid"]/div[5]/div/div[12]/div[2]/div[2]/div/div/img'

custom_dir = "/tmp/qrcodes"
os.makedirs(custom_dir, exist_ok=True)



async def scrape(username,password,chat_id):
    driver = get_driver()
    driver.get(url)
    name_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, name_xpath)))
    name_element.send_keys(username)
    password_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, password_xpath)))
    password_element.send_keys(password)
    login_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,login_xpath)))
    login_element.click()

    time.sleep(5)
    qr_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,qr_xpath))) # wait.until(EC.presence_of_element_located((By.XPATH, qr_xpath)))
    # print(qr_element.is_displayed)
    driver.execute_script("arguments[0].click();", qr_element) # force and js click event since div are not interactable in headless mode
    # qr_element.click()
    time.sleep(5)

    image_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,image_xpath)))
    src = image_element.get_attribute('src')
    image_name = str(today) + "-" + str(chat_id) + ".png"
    path_name = os.path.join(custom_dir,image_name)
    urllib.request.urlretrieve(src, path_name)

    return path_name

    driver.delete_all_cookies()
    driver.quit()





    

    # cookies = driver.get_cookies()
    # print(cookies)

    # driver.quit()

