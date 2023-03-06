from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        self.client = app.test_client()

    def test_home(self):

        with self.client:
            resp = self.client.get("/")
            self.assertIn("board", session)
            self.assertEqual(session.get("num_plays"), None)
            self.assertEqual(session.get("hs"), None)
            self.assertIn(b"Score:", resp.data)
            self.assertIn(b"Time left", resp.data)

    def test_valid_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [
                                ["x", "x", "x", "x", "x"],
                                ["x", "x", "x", "x", "x"],
                                ["x", "x", "x", "x", "x"],
                                ["x", "x", "x", "x", "x"],
                                ["C", "A", "R", "x", "x"],
                                ]
        response = self.client.get("/check?word=car")
        self.assertEqual(response.json["res"], "ok")

    
    def test_invalid_word(self):
        self.client.get("/")
        response = self.client.get("/check?word=catastrophe")
        self.assertEqual(response.json["res"], "not-on-board")

    def test_english_word(self):
        self.client.get("/")
        response = self.client.get("/check?word=abcde")
        self.assertEqual(response.json["res"], "not-word")