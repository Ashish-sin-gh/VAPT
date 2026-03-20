# Server Side Vulnerabilities

## 1. Path / Directory Traversal :

- **These vulnerabilities enable an attacker to read arbitrary files on the server that is running an application.**

- This might include:
    - application code and data.
    - credentials for back end system.
    - sensitive operating system file.

- Attack might **write** a file to the server.
    - modify app data / behaviour 
    - take full control of the server.


### How this vulnerability introduced in the code:

```
<?php
$template = 'blue.php';
if(isset($_COOKIE['TEMPLATE']))
    $template = $_COOKIE['TEMPLATE']
include("/home/users/phpguru/templates/" . $template);
?>
```
#### issue with the above code:
- no user input validation in the backend.

#### attack vector:
- Attack will set the cookie:
    > TEMPLATE=../../../../etc/passwd

- path made:
    > /home/users/phpguru/templates/../../../../etc/passwd

#### secure version:

```
$allowed = ['blue.php', 'red.php', 'green.php'];
if (isset($_COOKIE['TEMPLATE']) && in_array($_COOKIE['TEMPLATE'], $allowed)){
    $template = $_COOKIE['TEMPLATE'];
} else {
    $template = 'blue.php';
}
include("/home/users/phpguru/templates/" . $template);
```




### Reading arbitrary files via path traversal:

Example - 

- A shopping app - use following HTML to load product image:
    > \<img src="/loadImage?filename=218.png">

- The image are stored on a disk in the location 
    > /var/www/images/

- the above location is added to the image number to reutrn an image 
    > /var/www/images/218.png

- No defence againt `path traversal attack`

- attacker can request the following URL:
    > https://insecure-website.com/loadImage?filename=../../../etc/passwd

    - now the App will read the above file path
    - password exposed 
    - On Unix-based operating systems, this is a standard file containing details of the users that are registered on the server, 
    
- An attacker could retrieve other arbitrary files using the same technique. 

- in windows:
    > https://insecure-website.com/loadImage?filename=..\\..\\..\windows\win.ini

- The user get access to :
    - system users list | user info database
    - potential usernames (for brute force / SSH attacks)

