from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app=Flask(__name__)
app.config['SECRET_KEY']='key'
debug=DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO'] = True

def initialize():
    with app.app_context():
        connect_db(app)

initialize()

@app.route('/')
def home():
    '''redirects to list of users, will be corrected in later step'''
    return redirect('/users')

@app.route('/users')
def user_list():
    '''shows full list of users'''
    users = User.query.all()
    return render_template('user_listing.html', users=users)

@app.route('/users/new')
def new_user_form():
    '''shows new user form'''
    return render_template('create_user.html')

@app.route('/users/new', methods=["POST"])
def handle_new_user():
    '''handles new user info and '''
    fname=request.form['fname']
    lname=request.form['lname']
    img_url = request.form.get('img-url', None)
    if img_url == '':
        img_url = None
    new_user = User(first_name=fname, last_name=lname, image_url=img_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:id>')
def user_details(id):
    '''shows user detail page'''
    user = User.query.get(id)
    return render_template('user_details.html', user = user)

@app.route('/users/<int:id>/edit')
def edit_user(id):
    user = User.query.get(id)
    return render_template('user_edit.html', user = user)

@app.route('/users/<int:id>/edit', methods=["POST"])
def handle_edit(id):
    '''handles edit form submission'''
    user = User.query.get(id)
    user.first_name = request.form['fname']
    user.last_name = request.form['lname']
    user.image_url = request.form.get('img-url', None)
    if user.image_url == '':
        user.image_url = None
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:id>/delete', methods=['POST'])
def handle_delete(id):
    '''handles deletion of a user'''
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')