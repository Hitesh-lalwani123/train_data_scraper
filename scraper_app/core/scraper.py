from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import re


options = Options()
options.add_argument('--headless=new')  # Better headless mode
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
from scraper_app.db.db_connection import create_connection,insert_data,close_connection,clear_entry,update_progress
import time
from scraper_app.utils.constants import stations,FARE_CLASS,dates
from scraper_app.utils.util import expected_time,is_irctc_under_maintainance
from scraper_app import SCRAPER_URL

if(is_irctc_under_maintainance()):
    print("Irctc under maintainance currently")
def run_scraper(date_list = dates):
    print("scraping started")
    try:
        client = create_connection()
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        raise e

    def get_train_info(from_station: str, to_station: str,date: str):
        if(from_station == to_station):
            return []
        try:
            driver.get(SCRAPER_URL.format(from_station=from_station, to_station=to_station,date=date))
            wait = WebDriverWait(driver, 15)
            wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@id, 'train-')]"))
            )
            elements = driver.find_elements(By.XPATH, "//*[contains(@id, 'train-')]")
            result = []
            for val in elements:
                new_text = val.text
                result.append(new_text)
            if result:
                result.pop(0)
                return result
            else: 
                return []
        except Exception as e:
            raise e
        
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
        
    
    len_stations = len(stations) - 1
    records_processed = 0
    p1 = 0
    p2 = 0
    total_calls = (len_stations*(len_stations+1))/2 * len(date_list)
    print("total time: ", (total_calls*8)/60)
    completion_time = expected_time((total_calls*8)/60)
    print("Expected completion time: ",completion_time)
    driver.get(SCRAPER_URL.format(from_station="NGP", to_station="BPL",date="26-06-2025"))
    time.sleep(2)
    for curr_date in date_list:
        train_data = {}
        for p1 in range(len(stations)):
            for p2 in range(p1,len(stations)):
                if p1 == p2:
                    continue
                try:
                    trains = get_train_info(stations[p1],stations[p2],date=curr_date)
                    # time.sleep(2)
                   
                    result_list = generate_data(trains)
                    percent = (((records_processed + 1) / total_calls) * 100)
                    records_processed += 1
                    print("Progress: ",percent)
                    try:
                        update_progress(client,percent)
                    except Exception as e:
                        raise e
                
                    for train in result_list:
                        train_number = train['train_number']
                        data = train['data']
                        actual_from_st = train['from']
                        actual_to_st = train['to']
                        searched_from_st = stations[p1]
                        searched_to_st = stations[p2]
                        if train_number in train_data:
                            train_data[train_number][f"{searched_from_st}-{searched_to_st},{actual_from_st}-{actual_to_st}"] = data
                        else:
                            train_data[train_number]= {}
                            train_data[train_number][f"{searched_from_st}-{searched_to_st},{actual_from_st}-{actual_to_st}"] = data
                except Exception as e:
                    raise e
        try:       
            data = {curr_date: train_data}
            deleted_date= clear_entry(client,curr_date)
            print(deleted_date)
            object_id = insert_data(data,client)
            print(object_id)
        except Exception as e:
            raise e
    close_connection(client=client)
        
    driver.quit()

# run_scraper()


