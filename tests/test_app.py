from unittest import TestCase
from app import app
from mock import patch


class TestApp(TestCase):

    @patch("app.app.render_home")
    def test_home(self, render_home):
        render_home.return_value = 'success'
        self.assertEqual(app.home(), 'success')

    @patch("app.app.render_category")
    def test_category(self, render_category):
        render_category.return_value = 'success'
        file_name = 'dummy'
        self.assertEqual(app.category(file_name), 'success')
