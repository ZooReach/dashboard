from app.utils.dotdict import dotdict
from app.utils.extract_value import get_base_url_till_given_string
import unittest


class ExtractValue(unittest.TestCase):
    def test_get_base_url_till_given_string(self):
        request = dotdict({"base_url":"http://www.zooreach.com/category/bats"})
        string = 'category'
        self.assertEqual(get_base_url_till_given_string(request, string), "http://www.zooreach.com/category/")