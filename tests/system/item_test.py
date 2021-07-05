from models.item import ItemModel
from models.user import UserModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json

class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                res = client.post('/auth', 
                data=json.dumps({'username': 'test', 'password': '1234'}),
                headers = {'Content-Type': 'application/json'}
                )
                self.auth_token = f"JWT {json.loads(res.data)['access_token']}"
        
    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                res = client.get('/item/test')
                self.assertDictEqual({'message': 'Could not authorise, did you include a valid authorization header'}, json.loads(res.data))
                # self.assertEqual(res.status_code, 401)
    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                res = client.get('/item/test', headers = {'Authorization': self.auth_token})
                self.assertEqual(res.status_code, 404)



    def test_get_item_found(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 20, 1).save_to_db()
                res = client.get('/item/test', headers = {'Authorization': self.auth_token})
                self.assertEqual(res.status_code, 200)
                self.assertDictEqual({'name': 'test', 'price': 20}, json.loads(res.data))
    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 20, 1).save_to_db()
                res = client.delete('/item/test', headers = {'Authorization': self.auth_token})
                self.assertEqual(res.status_code, 200)
                self.assertIsNone(ItemModel.find_by_name('test'))
                self.assertDictEqual({'message': 'Item deleted'}, json.loads(res.data))
        
    def test_create_item(self):
        pass
    def test_create_item(self):
        pass
