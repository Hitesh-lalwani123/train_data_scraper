from datetime import datetime,timedelta
from datetime import time
import pytz

def expected_time(time_exp):
    ist = pytz.timezone("Asia/Kolkata")
    now_ist = datetime.now(ist)
    endtime = now_ist + timedelta(minutes=time_exp)
    return endtime