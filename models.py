from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

default_image_url = 'https://www.pngarts.com/files/10/Default-Profile-Picture-PNG-Transparent-Image.png' #find url

def connect_db(app):
    '''connects to database'''
    db.app=app
    db.init_app(app)
    db.drop_all()
    db.create_all()

class User(db.Model):
    '''creates a user table'''
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, nullable = False, default=default_image_url)

