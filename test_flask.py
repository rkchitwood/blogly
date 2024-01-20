from unittest import TestCase
from app import app
from models import db, User, Post


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['TESTING']=True
app.config['DEBUG_TB_HOSTS']=['dont-show-deubg-toolbar']



class AppTestCase(TestCase):
    '''tests app routes for functionality'''
    
    @classmethod
    def setUpClass(cls):
        with app.app_context():
            db.drop_all()
            db.create_all()


    def setUp(self):
        '''clean up existing users'''
        with app.app_context():
            User.query.delete()

            test_user = User(first_name='george', last_name='jungles')
            db.session.add(test_user)
            db.session.commit()
            self.id = test_user.id
            

            post = Post(title='cool title', content='really awesome content', user_id=self.id)
            db.session.add(post)
            db.session.commit()
            self.post_id=post.id

            self.client = app.test_client()

    def tearDown(self):
        '''clean up any fouled transaction'''
        with app.app_context():
            db.session.rollback()

    def test_base(self):
        '''tests for homepage redirect'''
        with self.client as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 302)
            response = client.get('/', follow_redirects=True)
            html = response.get_data(as_text=True)
            self.assertIn("george jungles", html)

    def test_user_listing(self):
        '''tests user listing page'''
        with self.client as client:
            response = client.get('/users')
            self.assertEqual(response.status_code, 200)
            html = response.get_data(as_text=True)
            self.assertIn("george jungles", html)

    def test_create_user(self):
        '''tests user creation page'''
        with self.client as client:
            response = client.get('/users/new')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<div id="form-container">\n        <form action="/users/new" id="new-user-form" method="POST">', html)

            data={"fname": "Ryan", "lname": "Chitwood"}
            resp=client.post("/users/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn("Ryan Chitwood", html)

    def test_user_details(self):
        '''tests user details page'''
        with self.client as client:
            response = client.get(f'/users/{self.id}')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn("george jungles", html)

    def test_post_form(self):
        '''tests creation of post'''
        with self.client as client:
            response = client.get(f'/users/{self.id}/posts/new')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)

            data={"title": "Banana", "content": "OOOH OOOH OOOH AAAH AAAH AAAH"}
            resp=client.post(f'/users/{self.id}/posts/new', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn("Banana", html)
            self.assertIn('cool title', html)


    def test_post_detail(self):
        '''tests post detail page'''
        with self.client as client:
            response = client.get(f'/posts/{self.post_id}')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('really awesome content', html)
            