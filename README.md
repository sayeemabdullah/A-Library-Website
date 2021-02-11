# A Library Website

## Backend:

### I used Python (Flask) to create RESTFul API and used Flask-SQLAlchemy [SQLite] for the database.
### For the token authentication I used JSON Web Token Authentication 1.7.1*

First, To create the database we have to run the following commands in the command prompt :

```console
A-Library-Website >python
>>from api import db
>>db.create_all()
>>exit()
```
#### N.B. IF YOU DON'T HAVE SQLITE OR SQLAlchemy INSTALLED PLEASE DO THAT FIRST

Once it is done and the database is created with the required tables you can use the following command to start the file :

```console
A-Library-Website >python api.py
```



##### * Recent versions have some bugs which may arise while decoding or encoding.  

