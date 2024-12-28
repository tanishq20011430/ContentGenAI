from flask_bcrypt import Bcrypt # type: ignore
from models.user_model import User, db

bcrypt = Bcrypt()

def create_user(username, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

def validate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    return None

def user_exists(username):
    return User.query.filter_by(username=username).first() is not None
