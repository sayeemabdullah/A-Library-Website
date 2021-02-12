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

The general user can - 

* login
* view books
* view specific book
* search books
* view wishlist
* add books in wishlist
* delete books from wishlist

The admin user can -

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

I have used werkzeug to ensure secure password and JSON Web Token Authentication to generate token which can be used to access a protected resource.


##### * Recent versions have some bugs which may arise while decoding or encoding.  

