import unittest
from code.topic_matching.app import is_relevant, match_content

class TestMatchingLogic(unittest.TestCase):

    def test_is_relevant(self):
        user_interest = {"type": "country", "value": "UK", "threshold": 0.24}
        content_tag = {"type": "country", "value": "UK", "threshold": 0.25}
        self.assertTrue(is_relevant(user_interest, content_tag))

        content_tag = {"type": "country", "value": "UK", "threshold": 0.26}
        self.assertTrue(is_relevant(user_interest, content_tag))

        content_tag = {"type": "country", "value": "UK", "threshold": 0.20}
        self.assertFalse(is_relevant(user_interest, content_tag))

    def test_match_content(self):
        users = [
            {
                "name": "John Dow",
                "interests": [
                    {"type": "instrument", "value": "VOD.L", "threshold": 0.5},
                    {"type": "country", "value": "UK", "threshold": 0.24}
                ]
            }
        ]

        content = [
            {
                "id": "123",
                "title": "My title",
                "content": "Some content about UK",
                "tags": [
                    {"type": "country", "value": "UK", "threshold": 0.25}
                ]
            },
            {
                "id": "124",
                "title": "Another title",
                "content": "Some content about USA",
                "tags": [
                    {"type": "country", "value": "USA", "threshold": 0.20}
                ]
            }
        ]

        matched_results = match_content(users, content)
        self.assertEqual(len(matched_results), 1)
        self.assertEqual(matched_results[0]['user'], 'John Dow')
        self.assertEqual(len(matched_results[0]['content']), 1)
        self.assertEqual(matched_results[0]['content'][0]['id'], '123')

if __name__ == '__main__':
    unittest.main()
