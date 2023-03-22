import json
import unittest
from app import app
import json


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_by_id(self):
        response = self.app.get(f'/data/1')
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/data/9999999')
        self.assertEqual(response.status_code, 404)

    def test_get_list(self):
        response = self.app.get('/data')
        self.assertEqual(response.status_code, 200)

    def test_active_filtering(self):
        # Test filtering by active status
        response = self.app.get('/data?active=true')
        data = json.loads(response.data)
        for provider in data:
            assert provider['active'] is True

        response = self.app.get('/data?active=false')
        data = json.loads(response.data)
        for provider in data:
            assert provider['active'] is False
