from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest

class TestStore(BaseTest):
    def test_create_store(self):
        store = StoreModel('test store')
        self.assertListEqual(store.items.all(), [])
    
    def test_crud(self):
        with self.app_context():
            store = StoreModel('test store')
            self.assertIsNone(StoreModel.find_by_name('test store'),
            "found a store before creating one")
            store.save_to_db()
            self.assertIsNotNone(StoreModel.find_by_name('test store'))
            store.delete_from_db()
            self.assertIsNone(StoreModel.find_by_name('test store'))
    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test store')
            item = ItemModel('test item', 12, 1)
            store.save_to_db()
            item.save_to_db()
            self.assertEqual(store.items.count(), 1)

    def test_store_json(self):
        with self.app_context():
            store = StoreModel('test store')
            store.save_to_db()
            expected = {
                'name': 'test store',
                'items': [],
                'id': 1
            }
            self.assertDictEqual(store.json(), expected)

    def test_store_multiple_items(self):
        with self.app_context():
            store = StoreModel('test store')
            item = ItemModel('test item', 20, 1)
            store.save_to_db()
            item.save_to_db()
        
            expected = {
                'name': 'test store',
                'items': [{'name': 'test item', 'price': 20}],
                'id': 1
            }
            self.assertDictEqual(store.json(), expected)