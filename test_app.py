from unittest import TestCase
from app import app
from flask import session


def test_home_page(self):
    with app.test_client() as client:
        # can now make requests to flask via `client`
        resp = client.get('/')
        # html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
