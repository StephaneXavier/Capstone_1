from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)



class Submitted_Data(db.Model):
    """Data submitted by user"""

    __tablename__ = "submitted_data"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    stopNo = db.Column(db.Integer,
                     nullable=False,
                     unique=False)
    busNo = db.Column(db.Integer, nullable=False)
    delay = db.Column(db.Integer, nullable=True)
    noShow = db.Column(db.Boolean, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    date_submitted = db.Column(db.DateTime, nullable=False)

    users = db.relationship('User',backref='submitted_data')

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    username = db.Column(db.String,
                     nullable=False,
                     unique=True)
    pwd = db.Column(db.String,
                     nullable=False,
                     unique=False)

    
    @classmethod
    def register(cls, username, pwd):
        hashed = bcrypt.generate_password_hash(pwd)

        hashed_utf8 = hashed.decode('utf8')

        return cls(username = username, pwd = hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.pwd, pwd):
            # return user instance
            return u
        else:
            return False


class Bus(db.Model):

    __tablename__ = 'buses'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    route_short_name = db.Column(db.String,
                     nullable=False,
                     unique=False)
    route_id = db.Column(db.String,
                     nullable=False,
                     unique=False)


class Stop(db.Model):

    __tablename__ = 'stops'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    stop_code = db.Column(db.String,
                     nullable=False,
                     unique=False)
    stop_name = db.Column(db.String,
                     nullable=False,
                     unique=False)