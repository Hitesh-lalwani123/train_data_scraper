
import time
from scraper_app.utils.constants import stations,FARE_CLASS,dates
from scraper_app.utils.util import expected_time,is_irctc_under_maintainance
from scraper_app import SCRAPER_URL

def generate_station_pairs():
    pairs= []
    for p1 in range(len(stations)):
        for p2 in range(p1,len(stations)):
            if p1 == p2:
                continue
            else:
                currpair = [stations[p1],stations[p2]]
                pairs.append(currpair)
    return pairs

def generate_url(pairs,date):
    urls = []
    for val in pairs:
        url = SCRAPER_URL.format(from_station=val[0], to_station=val[1],date = date)
        urls.append(url)
    return urls

def generate_batch(date):
    pairs = generate_station_pairs()
    URLS = generate_url(pairs,date)
    print(URLS)
    return URLS

