import unittest
from mock import patch

from app import app


class TestApp(unittest.TestCase):

    @patch("app.app.home")
    def test_render_home(self, r_home):
        r_home.render_home.return_value = 'success'
        self.assertEqual(app.home(), "success")
