from flask import Flask, request, jsonify, abort, g, url_for

from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

from passlib.apps import custom_app_context as pwd_context

import numpy
from word_loader import WordLoader

import os

app = Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY'] = 'TODO: FIXME'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)
auth = HTTPBasicAuth()

word_loader = WordLoader()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@app.route('/api/users', methods=['POST'])
def new_user():

    print(request.form)

    username = request.form.get('username')
    password = request.form.get('password')


    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})

@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@app.route("/api/words", methods=["GET"])
def hello():
    language = request.args["language"]
    real_words = int(request.args["realWords"])
    fake_words = int(request.args["fakeWords"])

    return jsonify({
        'realWords': [x.serialize() for x in get_real_words(language, real_words)],
        'fakeWords': [x.serialize() for x in get_fake_words(language, fake_words)]
    })

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/game.html')
def game():
    return app.send_static_file('game.html')

def get_real_words(language, real_words):
    words = word_loader.get_real_words_for(language=language)

    return list(numpy.random.choice(words, size=real_words, replace=False))

def get_fake_words(language, fake_words):
    words = word_loader.get_fake_words_for(language=language)

    return list(numpy.random.choice(words, size=fake_words, replace=False))

if __name__ == "__main__":
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run()