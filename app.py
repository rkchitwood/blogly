from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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
    user_posts = user.posts
    return render_template('user_details.html', user = user, posts = user_posts)

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
    # db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:id>/delete', methods=['POST'])
def handle_delete(id):
    '''handles deletion of a user'''
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:id>/posts/new')
def post_form(id):
    '''shows new post form for a user'''
    user = User.query.get(id)
    return render_template('post_form.html', user = user)

@app.route('/users/<int:id>/posts/new', methods=['POST'])
def handle_post(id):
    '''handles post form by adding post and redirecting to user detail page'''
    user = User.query.get(id)
    post = Post(title=request.form['title'], content=request.form['content'])
    user.posts.append(post)
    db.session.commit()
    return redirect(f'/users/{id}')

@app.route('/posts/<int:id>')
def post_details(id):
    '''shows a post'''
    post = Post.query.get(id)
    return render_template('post.html', post = post)

@app.route('/posts/<int:id>/edit')
def show_edit_post_form(id):
    '''shows the form to edit a post'''
    post = Post.query.get(id)
    username = post.user
    return render_template('post_edit_form.html', post = post, user=username)

@app.route('/posts/<int:id>/edit', methods=['POST'])
def handle_post_edit(id):
    '''updates a post based off of the edits to the post'''
    #retrieve post from db
    #update from form data
    #send to db
    post = Post.query.get(id)
    post.title = request.form['title']
    post.content = request.form['content']
    # db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{id}')

@app.route('/posts/<int:id>/delete', methods=['POST'])
def delete_post(id):
    '''deletes a post'''
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/users')
       