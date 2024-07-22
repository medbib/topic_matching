import unittest
from code.topic_matching.app import load_users, load_content

class TestApp(unittest.TestCase):

    def test_load_users(self):
        users = load_users()
        self.assertIsInstance(users, list)
        self.assertGreater(len(users), 0)
        self.assertIn('name', users[0])
        self.assertIn('interests', users[0])

    def test_load_content(self):
        content = load_content()
        self.assertIsInstance(content, list)
        self.assertGreater(len(content), 0)
        self.assertIn('id', content[0])
        self.assertIn('title', content[0])
        self.assertIn('content', content[0])
        self.assertIn('tags', content[0])

if __name__ == '__main__':
    unittest.main()
