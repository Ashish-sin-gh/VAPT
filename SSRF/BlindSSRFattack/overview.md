# Blind SSRF vulnerability

## Overview:

- Blind SSRF vulnerabilities occur if you can cause an application to issue a back-end HTTP request to a supplied URL, but the response from the back-end request is not returned in the application's front-end response. 

- hard to exploit

- can lead to remote code execution on server and other back end systems.

- The impact of blind SSRF vulnerabilities is often lower than fully informed SSRF vulnerabilities because of their one-way nature. 
    - cant retrieve sensitive data form the backend systems.

- Use `out-of-band` (OAST) technique:
    - Trigger an HTTP / DNS request to an external server that you (attacker) control
    - Monitor the network interactions with that system.

- use `Burp collaborator`.
    - Generate unique domain names.
    - send payloads to the application.
    - monitor for any interaction with those domains.
    -  **If an incoming HTTP request is observed coming from the application, then it is vulnerable to SSRF.**

### Use:

1. #### Leveraged to probe for other vulnerability on the server itself or other backend system.
    - You can blindly sweep the internal IP address space, sending payloads designed to detect well-known vulnerabilities.

2. #### Induce the application to connect to a system under the attacker's control
    - and return malicious responses to the HTTP client that makes the connection.

    - If you can exploit a serious client-side vulnerability in the server's HTTP implementation, you might be able to achieve remote code execution within the application infrastructure. 