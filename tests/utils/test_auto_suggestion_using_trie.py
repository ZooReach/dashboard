import unittest
from app.utils.auto_suggestion_using_trie import Node, autocomplete_main

class TestNode(unittest.TestCase):

    def setUp(self):
        self.root = Node()
        self.words = [{'name':'dear', 'id':1}, {'name':'deer', 'id':2}, {'name':'disco', 'id': 3}, {'name':'do', 'id': 4}, {'name':'anupriya', 'id': 5}]

    def test_add_word_to_trie(self):
        for word in self.words:
            self.root.add_word_to_trie(word.get("name").lower(), word.get("id"))
        self.assertEqual(len(self.root.children_node), 2)

    def test_auto_complete_word(self):
        for word in self.words:
            self.root.add_word_to_trie(word.get("name").lower(), word.get("id"))
        self.assertEqual(self.root.auto_complete_word('de'), [{'name':'dear', 'id':1}, {'name':'deer', 'id':2}])

    def test_autocomplete_main(self):
        autocompleted_words = autocomplete_main('de', self.words)
        self.assertEqual(autocompleted_words, [{'name':'dear', 'id':1}, {'name':'deer', 'id':2}])