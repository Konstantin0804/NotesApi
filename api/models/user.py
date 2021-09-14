from api import db, Config, ma
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from sqlalchemy.exc import IntegrityError


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    notes = db.relationship('NoteModel', backref='author', lazy='dynamic')
    # FIXME: server_default=False
    is_staff = db.Column(db.Boolean(), default=False,
                        server_default="false", nullable=False) # колонка у класса, которая будет говорить является ли юзер админов
    role = db.Column(db.String(32), default="simple_user", server_default="admin", nullable=False)

    def __init__(self, username, password, role="admin"):
        self.username = username
        self.hash_password(password)
        self.role = role

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(Config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    def get_roles(self):
        return self.role

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            print(f"User with username = {self.username} already exists")
            db.session.rollback()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(Config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = UserModel.query.get(data['id'])
        return user

    def __repr__(self):
        return f"User [{self.username}, {self.role}]"