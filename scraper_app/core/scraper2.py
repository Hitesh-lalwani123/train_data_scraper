from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import re
from scraper_app.db.db_connection import create_connection,insert_data,close_connection,clear_entry,update_progress
import time
from scraper_app.utils.constants import stations,FARE_CLASS,dates
from scraper_app.utils.util import expected_time,is_irctc_under_maintainance
from scraper_app import SCRAPER_URL
from scraper_app.core.generate_batch_urls import generate_batch
PROXIES = [
    "118.68.64.134:16000"
    ]
import random


if(is_irctc_under_maintainance()):
    print("Irctc under maintainance currently")


def get_driver(proxy=None):
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--disable-application-cache')
    chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--headless=new') 
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Basic stealth chrome_options
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Pretend to be a real user
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    # Disable extensions, pop-ups, and infobars
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    


    # Languages and platform to match real users
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # chrome_options.add_argument(
    #     '--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def run_scraper(correlation_id,date):
    print("scraping started")
    def get_train_info(url: str):
        try:
            proxy = random.choice(PROXIES)
            print(proxy)
            driver = get_driver(proxy)
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                })
            """
            })
            time.sleep(1)
            driver.get(url)
            print("started scraping for ",url)
            wait = WebDriverWait(driver, 15)
            wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@id, 'train-')]"))
            )
            wait = WebDriverWait(driver, 15)
            wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@id, 'train-')]"))
            )
            time.sleep(2)
            elements = driver.find_elements(By.XPATH, "//*[contains(@id, 'train-')]")
            
            result = []
            for val in elements:
                new_text = val.text
                result.append(new_text)
            driver.quit()
            if result:
                result.pop(0)
                print(result)
                return result
            else: 
                return []
        except Exception as e:
            raise "error getting info from confirm ticket"
        
    def generate_data(trains) -> list:
        results =[]
        if(trains):
            try:
                for train in trains:
                    train_data = train.split('\n')
                    if train_data[0] == "Nearby Station":
                        match = re.match(r"(\d+)(.*)", train_data[1])
                        train_no = match.group(1)
                        train_name = match.group(2)
                        from_station = train_data[3].strip().split(' ')[-1]
                        to_station = train_data[6].strip().split(' ')[-1]
                    else:
                        match = re.match(r"(\d+)(.*)", train_data[0])
                        train_no = match.group(1)
                        train_name = match.group(2)
                        from_station = train_data[2].strip().split(' ')[-1]
                        to_station = train_data[4].strip().split(' ')[-1]
                    train_res = {"train_number":train_no,"train_name":train_name,"data":{},"from":from_station,"to":to_station}
                    for i,data in enumerate(train_data):
                        try:
                            if(data.strip() in FARE_CLASS):
                                train_fare = train_data[i+1]
                                availibility = train_data[i+2]
                                train_res['data'][data] = [availibility,train_fare]
                        except:
                            pass
                    results.append(train_res)
            except Exception as e:
                print(e)
            return results    
        else:
            return results
        
    

    train_data = {}
    URLS = generate_batch(date)
    print(f"Starting parallel scraping of {len(URLS)} pages...")

    import time
    from concurrent.futures import ThreadPoolExecutor
    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            results = list(executor.map(get_train_info,URLS))
        print(len(results))
        print(type(results))
    except Exception as e:
        raise e

    print("\n✅ Scraping Complete!")
        
    


