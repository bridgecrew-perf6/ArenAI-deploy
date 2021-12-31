from django.core.checks.messages import ERROR
from django.db import connection
from django.template.response import ContentNotRenderedError
from django.test import TestCase
from rest_framework import response
import rest_framework
from ArenAI.response import SUCCESS_CODE, ERROR_CODE

# Create your tests here.

class TokenTest(TestCase):

    def setUp(self):
        response = self.client.post('/api/v1/auth/user', {
            'username': 'testuser',
            'password': '123456'
        })
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertEqual(content['code'], SUCCESS_CODE, msg=content)

    def test_correct_login(self):
        response = self.client.post('/api/v1/auth/token', {
            'username': 'testuser',
            'password': '123456'
        })
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertEqual(content['code'], SUCCESS_CODE, msg=content)
        
    def test_non_exist_user(self):
        response = self.client.post('/api/v1/auth/token', {
            'username': 'tesTuser',
            'password': '123456'
        })
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertEqual(content['code'], ERROR_CODE, msg=content)
        self.assertEqual(content['data']['msg'], "UserDoesNotExist", msg=content)

    def test_wrong_password(self):
        response = self.client.post('/api/v1/auth/token', {
            'username': 'testuser',
            'password': '1234567'
        })
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertEqual(content['code'], ERROR_CODE, msg=content)
        self.assertEqual(content['data']['msg'], "WrongPassword", msg=content)



class SignUpTest(TestCase):
    def test_dumplicate_sign_up(self):
        response = self.client.post('/api/v1/auth/user', {
            'username': 'testuser1',
            'password': '1234567'
        })
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertEqual(content['code'], SUCCESS_CODE, msg=content)

        response = self.client.post('/api/v1/auth/user', {
            'username': 'testuser1',
            'password': '12345678'
        })
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertEqual(content['code'], ERROR_CODE, msg=content)
        self.assertEqual(content['data']['msg'], "UserExist", msg=content)

    def test_unvalid_user_name(self):
        response = self.client.post('/api/v1/auth/user', {
            'username': '1',
            'password': '1234567'
        })
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertEqual(content['code'], ERROR_CODE, msg=content)
        self.assertEqual(content['data']['msg'], "UnvalidUserName", msg=content)

        response = self.client.post('/api/v1/auth/user', {
            'username': '?*_+',
            'password': '1234567'
        })
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertEqual(content['code'], ERROR_CODE, msg=content)
        self.assertEqual(content['data']['msg'], "UnvalidUserName", msg=content)

    def test_unvalid_password(self):
        response = self.client.post('/api/v1/auth/user', {
            'username': '1',
            'password': '1234567'
        })
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertEqual(content['code'], ERROR_CODE, msg=content)
        self.assertEqual(content['data']['msg'], "UnvalidUserName", msg=content)

        response = self.client.post('/api/v1/auth/user', {
            'username': '?*_+',
            'password': '1234567'
        })
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertEqual(content['code'], ERROR_CODE, msg=content)
        self.assertEqual(content['data']['msg'], "UnvalidUserName", msg=content)

class LoginStatusTest(TestCase):
    
    def setUp(self):
        response = self.client.post('/api/v1/auth/user', {
            'username': 'testuser3',
            'password': '123456'
        })
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertEqual(content['code'], SUCCESS_CODE, msg=content)
        
    def login_and_get_token(self):
        response = self.client.post('/api/v1/auth/token', {
            'username': 'testuser3',
            'password': '123456'
        })
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertEqual(content['code'], SUCCESS_CODE, msg=content)
        return content['data']['token']

    def test_get_user_name(self):
        token = self.login_and_get_token()
        response = self.client.get('/api/v1/auth/user', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertEqual(content['code'], SUCCESS_CODE, msg=content)
        self.assertEqual(content['data']['username'], 'testuser3', msg=content)

    def test_get_user_name_without_login(self):
        response = self.client.get('/api/v1/auth/user')
        self.assertEqual(response.status_code, 401)

    def test_logout(self):
        token = self.login_and_get_token()
        response = self.client.delete('/api/v1/auth/token', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertEqual(content['code'], SUCCESS_CODE, msg=content)
        self.assertEqual(content['data']['msg'], "LoggedOut", msg=content)

        response = self.client.get('/api/v1/auth/user', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 401)