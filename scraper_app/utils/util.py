from datetime import datetime,timedelta
from datetime import time
import pytz

def expected_time(time_exp):
    ist = pytz.timezone("Asia/Kolkata")
    now_ist = datetime.now(ist)
    endtime = now_ist + timedelta(minutes=time_exp)
    return endtime


def is_irctc_under_maintainance():
    
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

def generate_correlation_id():
    ist = pytz.timezone("Asia/Kolkata")
    now_ist = datetime.now(ist).time()
    time_str = str(now_ist)
    correlation_id_list = time_str.split('.')[0].split(':')
    correlation_id = "CORR"+"".join(correlation_id_list)
    return correlation_id
