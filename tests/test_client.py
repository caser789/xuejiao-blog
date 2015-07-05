import re
import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Role

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(user_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        # use get to request, and return a resposne
        response = self.client.get(url_for('main.index'))
        self.assertTrue(b'Stranger' in response.data)
        # or as unicode use response.get_data to access the reposne body 
        # self.assertTrue('Stranger' in response.get_data(as_text=True))

    def test_register_and_login(self):
        # register a new account
        response = self.client.post(url_for('auth.register'), data={
            'email': 'john@example.com',
            'username': 'john',
            'password': 'cat',
            'password2': 'cat'
            })
        # if success, redirect to login with 302
        self.assertTrue(response.status_code == 302 )

        # login with new accoutn
        response = self.client.post(url_for('auth.login'), data={
            'email': 'john@example.com',
            'password': 'cat'
            # use follow_redirects to auto send a get request, then get a
            # reponse instead of a redirect which return a 302
            }, follow_redirects=True) 
        # use re to \s+ --> at least a whitespace
        self.assertTrue(re.search(b'Hello,\s+john!', response.data))
        self.assertTrue(
                b'You have not confirmed your account yet' in response.data)

        # send a confirmation token
        user = User.query.filter_by(email='john@example.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token),
                                   follow_redirects=True)
        self.assertTrue(
                b'You have confirmed your account' in response.data)

        # log out
        response = self.client.get(url_for('auth.logout'),
                follow_redirects=True)
        self.assertTrue(b'You have been logged out' in response.data)
