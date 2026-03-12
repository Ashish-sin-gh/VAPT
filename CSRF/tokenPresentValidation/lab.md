# CSRF where token validation depends on token being present

### [vulneable website link](https://portswigger.net/web-security/learning-paths/csrf/csrf-common-flaws-in-csrf-token-validation/csrf/bypassing-token-validation/lab-token-validation-depends-on-token-being-present)

#### vulnerable parameter:
- email change functionality

#### exploit the CSRF vulerability
1. built an HTML page that use CSRF attack - change the email-address
2. Upload it to ur exploit server

### Analysis:

#### Is email change prone to CSRF attack?

1. #### is the functionality using cookie based session handling? -> YES

2. #### Do email change functionailty has a relevant action ? -> YES

    - Can change the users name and later change the password and have the control of the victims account.

3. #### presence of unpredictable parameter in the request ? -> YES
    - but it can be removed from the `POST` parameter and the application will skip the csrf validation.


### Testing CSRF tokens validation:

1. remove the CSRF token from the `POST` request parameter
2. Change the request method from `POST` to `GET`.