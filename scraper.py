from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
date = '08-08-2025'
options = Options()
options.add_argument('--headless=new')  # Better headless mode
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
import time
stations = [
    # # "YPR",
    # "YNK",
    # "HUP",
    # "DMM",
    # "ATP",
    # "DHNE",
    # "KRNT",
    # "MBNR",
    "KCG",
    # "HYB",
    # "KZJ",
    # "RDM",
    # "MCI",
    # "SKZR",
    # "BPQ",
    # "CD",
    "NGP",
    "BPL"]

# ,
#     "VGLJ",
#     "GWL",
#     "AGC",
#     "MTJ",
#     "BVH",
#     "NZM",
#     "NDLS"
# ]


def is_time_between_1145pm_and_1215am_ist():
    from datetime import datetime, time, timedelta
    import pytz
    # Get current time in IST
    ist = pytz.timezone("Asia/Kolkata")
    now_ist = datetime.now(ist).time()

    # Define start and end time
    start_time = time(23, 45)  # 11:45 PM
    end_time = time(0, 15)     # 12:15 AM

    # Handle the wrap-around midnight case
    if start_time <= now_ist or now_ist <= end_time:
        return True
    return False

if(is_time_between_1145pm_and_1215am_ist()):
    print("Irctc under maintainance currently")
    exit(1)


driver = webdriver.Chrome(options=options)
def get_train_info(from_station: str, to_station: str):
    if(from_station == to_station):
        return []
    FARE_CLASS = ['3A','2A']
    driver.get(f"https://www.confirmtkt.com/rbooking/trains/from/{from_station}/to/{to_station}/{date}")
    # print(driver.title)
    wait = WebDriverWait(driver, 15)
    time.sleep(5)
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
    
def generate_data(trains) -> list:
    import re
    if(trains):
        results =[]

        for train in trains:
            train_data = train.split('\n')
            match = re.match(r"^(\d+)(.*)", train_data[0])
            train_no = match.group(1)
            train_name = match.group(2)
            train_res = {"train_number":train_no,"train_name":train_name,"data":{}}
            for i,data in enumerate(train_data):
                try:
                    if(data in ['3A','2A','SL']):
                        train_res['data'][data] = train_data[i+2]
                except:
                    print(train_data)
            results.append(train_res)
        return results
    else:
        return []
final_result = []

for st in stations:
    trains = get_train_info(st,"BPL")
    time.sleep(2)
    result_list = generate_data(trains)
    final_data = {"date":date, "from":st,"to":'BPL',"train_data":result_list}
    final_result.append(final_data)

for val in final_result:
    
    from_st = val['from']
    to_st = val['to']
    train_data = val['train_data']
    if train_data == []:
        continue
    for train in train_data:
        data = train['data']
        train_no = train['train_number']
        train_name = train['train_name']
        for key in data:
            if data[key].split(' ')[0] in ['AVL','RAC']:
                print(train_no," ",train_name," ",from_st," ",to_st," ",key," ",data[key],"\n")
driver.quit()
