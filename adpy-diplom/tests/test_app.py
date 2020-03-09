import unittest
from unittest.mock import patch
import main
import json


class MyTestCase(unittest.TestCase):

    def setUp(self):
        with open('fixtures/info.json', 'r') as info:
            self.info = json.load(info)
        with open('fixtures/return_edit_keys.json', 'r') as edit_keys:
            self.return_edit_keys = json.load(edit_keys)
        with open('fixtures/return_info.json', 'r') as return_info:
            self.return_info = json.load(return_info)
        with open('fixtures/photos.json', 'r') as photos:
            self.photos = json.load(photos)
        with open('fixtures/return_top_photos.json', 'r') as return_top_photos:
            self.return_top_photos = json.load(return_top_photos)

    def test_edit_keys(self):
        result = main.edit_keys(**self.info)
        self.assertEqual(result, self.return_edit_keys)

    def test_user_info(self):
        with patch('main.input', side_effect=['20-29', 'Y', 'Y', '1']), patch('main.api') as mock:
            l_self_info = list()
            l_self_info.append(self.info)
            mock.users.get.return_value = l_self_info
            result = main.user_info()
            self.assertEqual(result, self.return_info)

    def test_top_photos(self):
        with patch('main.api') as mock:
            mock.photos.get.return_value = self.photos
            result = main.top_photos(70266597)
            self.assertEqual(result, self.return_top_photos)

if __name__ == '__main__':
    unittest.main()
