import unittest
from unittest.mock import patch
import app


class TestManageDocs(unittest.TestCase):
    def setUp(self):
        directories, documents = app.update_date()
        self.directories = directories
        self.documents = documents

    def test_update_date(self):
        res_directories, res_documents = app.update_date()
        self.assertIsInstance(res_directories, dict)
        self.assertIsInstance(res_documents, list)

    def test_add_doc_on_directories(self):
        len_doc = len(self.directories['2'])
        with patch('app.directories', self.directories) as moc:
            app.append_doc_to_shelf('12345', '2')
            self.assertLess(len_doc, len(moc['2']))

    def test_del_doc(self):
        len_doc = len(self.directories['1'])
        with patch('app.directories', self.directories) as moc:
            app.remove_doc_from_shelf("2207 876234")
            self.assertGreater(len_doc, len(moc['1']))

    def test_add_new_doc(self):
        len_dir = len(self.directories['2'])
        len_doc = len(self.documents)
        with patch('app.input', side_effect=['12345', 'passport', 'user', '2']), \
             patch('app.documents', self.documents)as moc_doc, \
             patch('app.directories', self.directories) as moc_dir:
            print(moc_dir)
            res = app.add_new_doc()
            print(moc_dir)
            self.assertEqual(res, '2')
            self.assertGreater(len(moc_dir['2']), len_dir)
            self.assertGreater(len(moc_doc), len_doc)


if __name__ == '__main__':
    unittest.main()
