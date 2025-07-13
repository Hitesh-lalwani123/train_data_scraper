import threading
import queue
import requests

q = []
valid_proxies = []

with open("free_proxies.txt",'r') as f:
    proxies = f.read().split("\n")
    for p in proxies:
        q.append(p)

def check_proxies():
    global q
    i = 0
    for val in q:
        if(i >= 30):
            break
        proxy = val
        try:
            res = requests.get("http://ipinfo.io/json",proxies={"http":proxy,"https":proxy})
        except:
            continue
        print(res.json())
        if res.status_code == 200:
            print(proxy)
        i = i+1


for _ in range(10):
    threading.Thread(target=check_proxies).start()