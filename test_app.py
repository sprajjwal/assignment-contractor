from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

""" TESTS BROUGHT OVER FROM PLAYLISTER TUTORIAL
(https://www.makeschool.com/academy/track/playlistr-video-playlists-with-flask-and-mongodb-1c)"""

sample_item_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_item = {
        'name': 'apple iphone x',
        'display_name': 'Apple iPhone X',
        'price': '700',
        'in_stock': '20',
        'images': ["sample_image_link"]
    }

class PlaylistsTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test route"""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the store's homepage route"""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Store', result.data)

    def test_new(self):
        """Test the new item creation page route"""
        result = self.client.get('/items/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Save Item', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_item(self, mock_find):
        """Test showing a single Item route"""
        mock_find.return_value = sample_item

        result = self.client.get(f'/items/{sample_item_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Price', result.data)
        self.assertIn(b'In stock', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_item_edit(self, mock_find):
        """Test editing a single Item route"""
        mock_find.return_value = sample_item

        result = self.client.get(f'/items/{sample_item_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Price', result.data)
        self.assertIn(b'In stock', result.data)

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_items_delete(self, mock_delete):
        """ Test deleting a single item route"""
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/items/{sample_item_id}/delete', data=sample_item)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_item_id})

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_items(self, mock_update):
        """Test Update function on the POST route"""
        result = self.client.post(f'/items/{sample_item_id}', data=sample_item)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_item_id}, {'$set': sample_item})

if __name__ == '__main__':
    unittest_main()