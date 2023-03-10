import unittest
from app import app
from database import db

class TestApp(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.data.decode('utf-8'), 'Hello, World!')

    def test_get_cards(self):
        response = self.client.get('/cards')
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.json, [])

    def test_get_columns(self):
        response = self.client.get('/columns')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, ['To Do', 'Doing', 'Done'])
    
    def test_create_card(self):
        response = self.client.post('/card', data={
            'text': 'Test Card',
            'column': 'To Do',
            'color': 'red',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Success')

    def test_delete_card(self):
        response = self.client.delete('/card/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Success')

    def test_store_user():
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
