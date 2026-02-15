# DIRB Tool | DirB
uster | Directory Buster

## Using DirBuster on websites without permission is illegal.

A command-line web content scanner used by security professionals to **find hidden files and directories** on a web server.

#### Sometimes, applications will expose sensitive functionality to users via secret URLs.

### Used in **Reconnaissiance phase** to uncover:
- hidden URLs
- hidden directories
- unlinked files
- backup files
- configuration files
- admin panels
- unlinked endpoints

### Dictionary-based brut forcing attacks.

DirBuster tries thousands of common names automatically to find them.

### What happen in backend:
- uses a word list

    ```
    /admin
    /backup
    /test
    /config
    /uploads
    ```
- Append each word of the URL.

    > example.com/admin  
    example.com/test  
    example.com/backup

- Checks the server response   
- report valid directories/files

launch HTTP requests to the target

analyzing the responses to enumerate valid resources. 

### Modern alternative:

- goBuster
- FFUF
- Dirsearch
- WFuzz