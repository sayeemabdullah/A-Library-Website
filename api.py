from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
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
    name = db.Column(db.String(50))
    author = db.Column(db.String(50))
    publication_year = db.Column(db.Integer)

class Wishlist(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer)


@app.route('/user', methods=['GET'])
def get_all_users():

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


@app.route('/user/<public_id>', methods=['GET'])
def get_one_user(public_id):

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


@app.route('/user', methods=['POST'])
def create_user():

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
        
    users = User.query.all()

    for user in users:
        if data['name'] == user.name:
            return jsonify({'message' : 'User already exist'})           


    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user has been created'})


@app.route('/user/<public_id>', methods=['PUT'])
def promote_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'User not found'})
    else:
        user.admin = True
        db.session.commit()
        return jsonify({'message' : 'User updated to Admin'})


@app.route('/user/<public_id>',methods=['DELETE'])
def delete_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'User not found'})
    else:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message' : 'User deleted'})


if __name__ == '__main__':
    app.run(debug=True)