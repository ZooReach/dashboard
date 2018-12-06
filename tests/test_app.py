import unittest
from mock import patch

from app import app


class TestApp(unittest.TestCase):

    @patch("app.app.render_home")
    def test_render_home(self, render_home):
        render_home.return_value = 'success'
        self.assertEqual(app.home(), "success")
