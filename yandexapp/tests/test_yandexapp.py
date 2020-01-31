import unittest
from unittest.mock import patch
import yandexapp


class TestYandexApp(unittest.TestCase):
    def test_response_yandex_api(self):
        result = yandexapp.response_yandex_api('Привет, мир!')
        self.assertEqual(result['code'], 200)
        self.assertEqual(result['text'][0], 'Hello world!')

    def test_wrong_api_yandex(self):
        with patch('yandexapp.API_KEY', ''):
            result = yandexapp.response_yandex_api('Привет')
            self.assertEqual(result['code'], 401)


if __name__ == '__main__':
    unittest.main()
