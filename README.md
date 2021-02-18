# A Library Website

## Backend:

#### I used Python (Flask) to create RESTFul API and used Flask-SQLAlchemy [SQLite] for the database.
#### For the token authentication I used JSON Web Token Authentication 1.7.1*

To create the database we have to run the following commands in the command prompt :

```console
A-Library-Website >python
>>from api import db
>>db.create_all()
>>exit()
```
Or you can use the existing database which is **recommended**.

##### N.B. IF YOU DON'T HAVE SQLITE OR/AND SQLAlchemy INSTALLED PLEASE DO THAT FIRST

Once it is done and the database is created with the required tables you can use the following command to start the file :

```console
A-Library-Website >python api.py
```


### Users:

There are two types of users one is general user and another is admin user. 

The **general user** can - 

* login
* view books
* view specific book
* search books
* view wishlist
* add books in wishlist
* delete books from wishlist

The **admin user** can -

* login
* add admin
* view all user
* view specific user
* delete user
* add books
* edit books
* delete books
* view books
* view specific book 
* search books
* view wishlist
* add books in wishlist
* delete books from wishlist

### Security:

I have used **Werkzeug** to ensure secure password and **JSON Web Token Authentication** to generate token which can be used to access a protected resource.

### Test the APIs on Postman:

To use the admin user you can use admin as both name and password to login by using **http://127.0.0.1:5000/api/login**. After tha a **token** will be generated which
will be need in during testing other functionality. The token is to be used as **x-access-token** in the **header**. You can also sign up as general user by posting 
**http://127.0.0.1:5000/api/user** & sending json file and request PUT to promote user to Admin or request DELETE to delete user by only if you are logged in as admin.
Beside that both the user can use **/api/book** and **/api/wishlist** to test other functionality. 



##### * Recent versions have some bugs which may arise while decoding or encoding. 

