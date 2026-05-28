import unittest
from app import create_app, db
from app.models import User, Document

class CRSCWPTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_signup_duplicate_check(self):
        # Test signup
        response = self.client.post('/signup', data=dict(
            email='test@example.com',
            name='Tester',
            password='password'
        ), follow_redirects=True)
        self.assertIn(b'\xeb\xa1\x9c\xea\xb7\xb8\xec\x9d\xb8', response.data) # Check for '로그인' in Korean

        # Test duplicate signup
        response = self.client.post('/signup', data=dict(
            email='test@example.com',
            name='Tester2',
            password='password'
        ), follow_redirects=True)
        self.assertIn(b'\xec\x9d\xb4\xeb\xaf\xb8 \xeb\x93\xb1\xeb\xa1\x9d\xeb\x90\x9c', response.data) # '이미 등록된'

    def test_login_and_2fa_simulation(self):
        # Signup first
        self.client.post('/signup', data=dict(
            email='test@example.com',
            name='Tester',
            password='password'
        ))
        
        # Login
        response = self.client.post('/login', data=dict(
            email='test@example.com',
            password='password'
        ), follow_redirects=True)
        self.assertIn(b'2\xeb\x8b\xa8\xea\xb3\x84 \xec\x9d\xb8\xec\xa6\x9d', response.data) # '2단계 인증'
        
        # Verify 2FA
        response = self.client.post('/2fa/1', data=dict(code='123456'), follow_redirects=True)
        self.assertIn(b'\xed\x94\x84\xeb\xa1\x9c\xed\x95\x84', response.data) # '프로필'

if __name__ == '__main__':
    unittest.main()
