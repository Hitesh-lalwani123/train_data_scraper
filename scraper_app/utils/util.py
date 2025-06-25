from datetime import datetime,timedelta
from datetime import time
import pytz

def expected_time(time_exp):
    ist = pytz.timezone("Asia/Kolkata")
    now_ist = datetime.now(ist)
    endtime = now_ist + timedelta(minutes=time_exp)
    return endtime


def is_irctc_under_maintainance():
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