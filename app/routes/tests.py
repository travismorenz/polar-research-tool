import json
import unittest
from app.models import db
from app.worker import app


class BackendTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        db.create_all()

    def test_articles_by_id(self):
        response = self.client.post('/api/articles-by-id', )
        self.assertEqual(response.status_code, 200)

    def test_get_article_ids(self):
        response = self.client.get('/api/article-ids', )
        self.assertEqual(response.status_code, 200)

    def test_get_articles_by_library(self):
        response = self.client.get('/api/articles-by-library/project_id', )
        self.assertEqual(response.status_code, 200)

    def test_toggle_in_library(self):
        response = self.client.post('/api/toggle-in-library/project_id', )
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
