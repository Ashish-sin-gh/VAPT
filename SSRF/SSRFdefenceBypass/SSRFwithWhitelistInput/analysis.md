# SSRF with Whitelist based input filters

### [vulnerable lab]()

## Overview:

- Some applications only allow inputs that match, a **whitelist of permitted values**. 

- The filter may look for a match at the beginning of the input, 
    ```
    if url.startswith("https://trusted.com"):  
        allow()
    ```

- or contained within in it. 
    ```
    if "trusted.com" in url:
        allow()
    ```

- ### Dev only match the string 
    - instead of acutal `URL parsing + validation` 

### <u>BYPASS</u>:

1. You can embed credentials in a URL before the hostname, using the `@`.

    > https://expected-host:fakepassword@evil-host

2. You can use the `#` to indicate a URL fragment.
    - content after `#` is not send to the server.

    > https://evil-host#expected-host

3. You can leverage the DNS naming hierarchy to place required input into a fully-qualified DNS name that you control.
    - create a domain that has both trusted value and attackers control.

    > trusted.com.evil.com

    - server connect to `evil.com` not `trusted.com`

4. You can URL-encode characters to confuse the URL-parsing code.

### Prevention:

- Exact hostname match karo:
    > trusted.com == hostname
- Avoid subdomain confusion 
- Use proper URL parsing 
- Use strict Allowlist