from models.store import StoreModel
from tests.base_test import BaseTest
import json
from models.item import ItemModel
class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                res = client.post('/store/test')
                self.assertEqual(res.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'name': 'test', 'items': [], 'id': 1}, json.loads(res.data))
    def test_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                res = client.post('/store/test')
                self.assertEqual(res.status_code, 400)
                self.assertDictEqual({'message': "A store with name '{}' already exists.".format('test')}, json.loads(res.data))
    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                res = client.delete('/store/test')
                self.assertEqual(res.status_code, 200)
                self.assertIsNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'message': 'Store deleted'}, json.loads(res.data))
    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                res = client.get('/store/test')
                self.assertEqual(res.status_code, 200)
                self.assertDictEqual({'name': 'test', 'items': [], 'id': 1}, json.loads(res.data))
    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                res = client.get('/store/test')
                self.assertEqual(res.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'}, json.loads(res.data))
    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 20, 1).save_to_db()
                res = client.get('/store/test')
                self.assertEqual(res.status_code, 200)
                self.assertEqual({'name': 'test', 'id': 1, 'items': [{'name': 'test', 'price': 20}]}, json.loads(res.data))
