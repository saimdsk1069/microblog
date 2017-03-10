from app import db, lm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from hashlib import md5

class User(UserMixin, db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  social_id = db.Column(db.String(64), nullable= False, unique=True)
  nickname = db.Column(db.String(64), nullable=False, unique=True)
  email = db.Column(db.String(64), nullable=True)
  posts = db.relationship('Post', backref='author', lazy='dynamic')
  about_me = db.Column(db.String(140))
  last_seen = db.Column(db.DateTime)
  
  def avatar(self, size):
    if self.email:
      return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)
    return None
  
  @staticmethod
  def make_unique_nickname(nickname):
    if User.query.filter_by(nickname=nickname).first() is None:
      return nickname
    version = 2
    while True:
      new_nickname = nickname + str(version)
      if User.query.filter_by(nickname = new_nickname).first() is None:
        break
      version += 1
    return new_nickname

@lm.user_loader
def load_user(id):
  return User.query.get(int(id))

"""class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.nickname)
"""
class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.String(140))
  timestamp = db.Column(db.DateTime)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  
  def __repr__(self):
    return '<post %r>' % (self.body)

  
  