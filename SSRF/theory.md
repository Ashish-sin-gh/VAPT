# SSRF - Server Side Request Forgery 

## What is SSRF?

- Server-side request forgery is a web security vulnerability that allows an attacker to cause the **server-side application to make requests to an unintended location**. 

- Occurs when an app is fetching a remote resource w/o first validating the user-supplied URL.

- attacker coerce the server into making network connections on behave of the attacker and potentially target system that are behind the firewall.

## blue teaming - watch out for:
- if logs show URL parameter request contaning :
    - IP address,
    - hostname,
    - or URL 
- test it for SSRF attack.

## Usage: 

### Expolit user supplied parameter:

- URL parameters are **user controllable** - can be changed by the client / user client side.

- **Not properly validated** - limited to no logic is being applied at the back end to block malicious payload.

    ![SSRF](./images/SSRFdiagram.png)

### SSRF is also used for port scan of the network:

- SSRF vulnerabilty can be used to run an **automated attack** that scan the entire pvt. IP range for server that are running application.

- Which port is up.

- what services are running on the up ports.

- attacker can **access internal services**.
    - `localhost` | `127.0.0.1`

    - Private IPs (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`)

    - that are not accessible via internet.

    ![port scan](./images/portScan.png)

### Exploit SSRF vulnerabilty that are present in application running the cloud  

- use to steal `cloud metadata`.

- example:
    - app in AWS
    - > http://169.254.169.254/latest/meta-data/
    - attack get access of:
        - access keys
        - IAM roles
        - secrets

## Type of SSRF :

```
                       [SSRF]
                      /      \
    [Regular / In Band]       [Blind / Out-of-Band]
```

1. **Regular / In band :**
    - Attacker can tamper with the requested URL and the response to the requested URL can be displayed back to the attacker.

2. **Blind / out-of-band :**
    - Attacker can tamper wiht the requested URL and the response to the requested URL CAN NOT be displayed back to the attacker.

    - In order to prove that the vulnerabilty does really exist, attacker will force a `DNS` or `HTTP` request from  the victim app to attacker controlled server (eg - Burp colaborator).
        - If the attacker server **gets** the request - **SSRF present**.
        - If the attacker server **dont get** the request - **SSRF not present**

## How to find SSRF vulnerabilities:

### Black Box POV:

- 