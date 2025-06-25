
import unittest
import os
import sqlite3
from app import app, get_db_connection, init_db, DATABASE

class FlaskAppTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        if os.path.exists(DATABASE):
            os.remove(DATABASE)
        init_db()

    def tearDown(self):
        if os.path.exists(DATABASE):
            os.remove(DATABASE)

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Posts', response.data)
        self.assertIn(b'Create New Post', response.data)

    def test_create_post(self):
        response = self.app.post('/create', data={'title': 'Test Title', 'content': 'Test Content'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Title', response.data)
        self.assertIn(b'Test Content', response.data)

        conn = get_db_connection()
        post = conn.execute('SELECT * FROM posts WHERE title = "Test Title"').fetchone()
        conn.close()
        self.assertIsNotNone(post)
        self.assertEqual(post['content'], 'Test Content')

    def test_create_post_no_title(self):
        response = self.app.post('/create', data={'title': '', 'content': 'Test Content'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Title is required!', response.data)

if __name__ == '__main__':
    unittest.main()
