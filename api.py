from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
# import os

# python api.py
# sqlite3 alw.db

app = Flask(__name__)

# file_path = os.path.abspath(os.getcwd())+"\alw.db"

app.config['SECRET_KEY'] = 'xxxx'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\A-Library-Website\\alw.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    author = db.Column(db.String(50))
    publication_year = db.Column(db.Integer)

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wishlist_public_id = db.Column(db.String(50), unique=True)
    user_public_id = db.Column(db.Integer)
    book_public_id = db.Column(db.Integer)



# TOKEN -- STARTS --

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token not found!'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            # return jsonify({'message' : data}), 401
            current_user = User.query.filter_by(public_id = data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# TOKEN -- ENDS --

# USER -- STARTS --   

@app.route('/api/user', methods=['GET'])
@token_required 
def get_all_users(current_user):

    if not current_user.admin:
        return jsonify({'message' : 'You are not authorized.'})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name']  = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users' : output})


@app.route('/api/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):

    if not current_user.admin:
        return jsonify({'message' : 'You are not authorized.'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'User not found'})
    else:
        output = []
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name']  = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
        return jsonify({'users' : output})


@app.route('/api/user', methods=['POST'])
def create_user():

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
        
    users = User.query.all()

    data['name'] = data['name'].upper()

    for user in users:
        if data['name'] == user.name:
            return jsonify({'message' : 'Username already exist'})           


    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user has been created'})


@app.route('/api/user/<public_id>', methods=['PUT'])
@token_required 
def promote_user(current_user, public_id):

    if not current_user.admin:
        return jsonify({'message' : 'You are not authorized.'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'User not found'})
    else:
        user.admin = True
        db.session.commit()
        return jsonify({'message' : 'User upgraded to Admin'})


@app.route('/api/user/<public_id>',methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):

    if not current_user.admin:
        return jsonify({'message' : 'You are not authorized.'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'User not found'})
    else:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message' : 'User deleted'})


# USER -- ENDS -- 

# BOOK -- STARTS --

@app.route('/api/book', methods=['GET'])
@token_required
def view_all_books(current_user):


    books = Book.query.all()

    output = []

    for book in books:
            book_data = {}
            book_data['book_public_id']  = book.book_public_id
            book_data['name']  = book.name
            book_data['author'] = book.author
            book_data['publication_year'] = book.publication_year
            output.append(book_data)

    return jsonify({'books' : output})


@app.route('/api/book/<book_public_id>', methods=['GET'])
@token_required
def view_one_book(current_user, book_public_id):


    book = Book.query.filter_by(book_public_id=book_public_id).first()

    output = []

    book_data = {}
    book_data['book_public_id']  = book.book_public_id
    book_data['name']  = book.name
    book_data['author'] = book.author
    book_data['publication_year'] = book.publication_year
    output.append(book_data)
            

    return jsonify({'books' : output})


@app.route('/api/book', methods=['POST'])
@token_required
def add_book(current_user):

    if not current_user.admin:
        return jsonify({'message' : 'You are not authorized.'})
    
    data = request.get_json()
       
    books = Book.query.all()

    data['name'] = data['name'].upper()

    for book in books:
        if data['name'] == book.name:
            return jsonify({'message' : 'Book is already in the library'})           


    new_book = Book(book_public_id=str(uuid.uuid4()),name=data['name'], author=data['author'], publication_year=data['publication_year'])

    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message' : 'New book has been added'})


@app.route('/api/book/<book_public_id>',methods=['DELETE'])
@token_required
def delete_book(current_user, book_public_id):

    if not current_user.admin:
        return jsonify({'message' : 'You are not authorized.'})

    book = Book.query.filter_by(book_public_id=book_public_id).first()

    if not book:
        return jsonify({'message' : 'Book not found'})
    else:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message' : 'Book deleted'})


@app.route('/api/book/<book_public_id>', methods=['PUT'])
@token_required 
def update_book(current_user, book_public_id):

    if not current_user.admin:
        return jsonify({'message' : 'You are not authorized.'})

    book = Book.query.filter_by(book_public_id=book_public_id).first()

    data = request.get_json()

    if not book:
        return jsonify({'message' : 'Book not found'})
    else:
        book.name = data['name']
        book.author = data['author']
        book.publication_year = data['publication_year'] 
        db.session.commit()
        return jsonify({'message' : 'Book updated'})

# BOOK -- ENDS --

# SEARCH -- STARTS --

@app.route('/api/book/search',methods=['GET'])
@token_required 
def search_book(current_user):

    data = request.get_json()

    data['name'] = data['name'].upper()

      
    book = Book.query.filter_by(name=data['name']).first()
    # output = Book.query.filter(Book.name.contains(data['name'])).all()
    # book = Book.query.filter_by(Book.name.like('%'+data['name']+'%'))

    if not book:
        return jsonify({'message' : 'No match found'})

    output = []

    book_data = {}
    book_data['book_public_id']  = book.book_public_id
    book_data['name']  = book.name
    book_data['author'] = book.author
    book_data['publication_year'] = book.publication_year
    output.append(book_data)
            

    return jsonify({'books' : output})


# SEARCH -- ENDS --

# WISHLIST -- STARTS --

@app.route('/api/wishlist/<book_public_id>', methods=['POST'])
@token_required
def add_wishlist(current_user, book_public_id):
    
    new_wishlist = Wishlist(wishlist_public_id=str(uuid.uuid4()),user_public_id=current_user.public_id, book_public_id=book_public_id)
    db.session.add(new_wishlist)
    db.session.commit()

    return jsonify({'message' : 'New wishlist has been added'})


@app.route('/api/wishlist', methods=['GET'])
@token_required
def view_all_wishlists(current_user):


    wishlists = Wishlist.query.filter_by(user_public_id=current_user.public_id)
    

    output = []

    for wishlist in wishlists:
            wishlists_data = {}
            wishlists_data['wishlist_public_id']  = wishlist.wishlist_public_id
            # wishlists_data['user_public_id']  = wishlist.user_public_id
            wishlists_data['book_public_id'] = wishlist.book_public_id
            books = Book.query.filter_by(book_public_id=wishlist.book_public_id)
            for book in books:
                if wishlist.book_public_id == book.book_public_id:
                    # wishlists_data['book_public_id']  = book.book_public_id
                    wishlists_data['name']  = book.name
                    wishlists_data['author'] = book.author
                    wishlists_data['publication_year'] = book.publication_year

            output.append(wishlists_data)

    return jsonify({'wishlists' : output})

@app.route('/api/wishlist/<wishlist_public_id>',methods=['DELETE'])
@token_required
def delete_book_from_wishlist(current_user, wishlist_public_id):

    wishlist = Wishlist.query.filter_by(wishlist_public_id=wishlist_public_id).first()

    if not wishlist:
        return jsonify({'message' : 'Wishlist not found'})
    else:
        db.session.delete(wishlist)
        db.session.commit()
        return jsonify({'message' : 'Wishlist deleted'})


# WISHLIST -- ENDS --

# LOGIN -- STARTS --

@app.route('/api/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify',401,{'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username.upper()).first()

    if not user:
        return make_response('Could not verify',401,{'WWW-Authenticate' : 'Basic realm="Login required!"'})
    
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})
    
    return make_response('Could not verify',401,{'WWW-Authenticate' : 'Basic realm="Login required!"'})

# LOGIN -- ENDS --

if __name__ == '__main__':
    app.run(debug=True)