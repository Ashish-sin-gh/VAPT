# CSRF (Cross Site Request Forgery) vulnerability

image credit - [Rana Khalil](https://www.youtube.com/@RanaKhalil101)

## What is CSRF?
Is a web-security vulnerability that allow an attacker to induce users to perform an action that they do not intend to perform.

Attacker partially circumvent **same origin policy**.
- ***one website cant access data of other website.*** 
- partial circumvent means:
    - attacker cant access/read data.
    - attacker can request to modify data.

- CSRF breach trust of the browser. 

## cookies: 
simply a text file that contains some information that identifies the user to the backend

**many application uses cookies that contains users PII.**
- username 
- roles of the user in the application - access privilage
- etc etc

![seesion management](./images/session%20management)

This cookie identify the user for all future requests.

### How cookie work in the backend:

![cookie backend](./images/how%20cookie%20work.png)

1. user accesses a domain he has accessed before.
2. brower check the `cookie jar`
3. if cookie exist for same domain - browser send it with the `get request`.
4. domain's backend check which user is assigned to this cookie
5. application check for level of access to the user.
6. and give access to the resources.


#### important pre-requisite:  
user has to be already logged in to the application. 

## Steps to CSRF attack:

**1. attacker send the victim a malicious link that will conduct the CSRF attack.**

![send phising mail](./images/step1CSRF.png)
    sent a phising link - will change the users email address registerd on the bank website.

**2. if user is authenticated - has a cookie in the cookies jar for `bank website` , attacker can change the email** 

![victim sent request to website](./images/step2CSRF.png)

**3. attack now has direct access to the users account.**

![attacker direct manipulation](./images/step3CSRF.png)

## CSRF conditons:
for a webiste to be tagged as vulnerable to CSRF:

1. **A relevent action** - an expolit that will cause detrimental effect to the victim.  
    example - logout functionality / change language functionality - it not serious enough. Hence not CSRF vulnerable.

2. **Cookie based session handling** - CSRF is depend on the default functionality of the browser to send cookies with the requests.

3. **No unpredictable request parameters** - attacke must be able to predict the URL parameter. 
    - example- `https://bank.com/email/chnage?email=attacker@gmail.com`
    - the paramete (email) here is predictable 

    hence to defend from CSRF attack - **`CSRF token`** is added with the request parameter.

## How to find CSRF vulnerabilty:

### Prespective:

- **Black box testing** -   
    Tester is given:
    - URL of the application
    - Credentials for each access level of the app

- **White Box Testing** - 
    Tester is given: (more visibility)
    - URL
    - creds
    - source code 

### Black Box prespective:

#### 1. Map the app

- review all the key functionality in the app

#### 2. Identify which of the functionality satisfy the condition:
- relevent actions
- cookie-based session handling
- no unpredictable request parameters

#### 3. create a PoC (Proof of Concept) script to the exploit CSRF
- `GET` request : `<img>` tag with `src` attribute set to vulnerbale URL.
    
- `POST` request : `form` elements with hidden fields for all required parameters and the target set to vulnerable URL

### White Box prespective:

#### 1. identify the framework that is being used by the application 
- read the code
- modern frameworks have build in defences for CSRF vulnerability 

#### 2. findout how the frame work defence againt CSRF attacks

#### 3. review the code to ensure the built in defenses have not been disabled 
- devs do this while integreting their app with other app

#### 4. review each and every functionality to ensure that the CSRF defense has been applied 
- some times dev intoduce custom code etc