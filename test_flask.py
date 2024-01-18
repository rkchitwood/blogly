from unittest import TestCase
from app import app
from models import db, User


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.config['TESTING']=True
app.config['DEBUG_TB_HOSTS']=['dont-show-deubg-toolbar']



class AppTestCase(TestCase):
    '''tests app routes for functionality'''

    def beforeAll(self):
        with app.app_context():
            db.drop_all()
            db.create_all()


    def setUp(self):
        '''clean up existing users'''
        with app.app_context():
            User.query.delete()

            user = User(first_name='george', last_name='jungles')
            db.session.add(user)
            db.session.commit()
            self.id = user.id
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