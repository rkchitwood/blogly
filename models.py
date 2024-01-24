from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

default_image_url = 'https://www.pngarts.com/files/10/Default-Profile-Picture-PNG-Transparent-Image.png' #find url

def connect_db(app):
    '''connects to database'''
    db.app=app
    db.init_app(app)
    #db.drop_all()
    db.create_all()

class User(db.Model):
    '''creates a users table'''
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, nullable = False, default=default_image_url)
    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan', passive_deletes=True)

class Post(db.Model):
    '''creates a posts table'''
    __tablename__='posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

class Tag(db.Model):
    '''creates a tag table'''
    __tablename__='tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable = False)
    posts = db.relationship('Post', secondary='posts_tags', backref='tags')

class PostTag(db.Model):
    '''creates m:m join of post and tag table'''
    __tablename__='posts_tags'
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
