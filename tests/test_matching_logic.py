import unittest
from code.topic_matching.backend.app import is_relevant, match_content, match_without_threshold, get_alternative_suggestions

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


class TestMatchingLogicWithoutThreshold(unittest.TestCase):

    def test_match_without_threshold(self):
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
                    {"type": "country", "value": "UK", "threshold": 0.20}
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

        matched_results = match_without_threshold(users, content)
        self.assertEqual(len(matched_results), 1)
        self.assertEqual(matched_results[0]['user'], 'John Dow')
        self.assertEqual(len(matched_results[0]['content']), 1)
        self.assertEqual(matched_results[0]['content'][0]['id'], '123')

    def test_get_alternative_suggestions(self):
        users = [
            {
                "name": "Jane Doe",
                "interests": [
                    {"type": "instrument", "value": "AAPL", "threshold": 0.5},
                    {"type": "country", "value": "USA", "threshold": 0.3}
                ]
            }
        ]

        content = [
            {
                "id": "125",
                "title": "Apple in the USA",
                "content": "Content about Apple in the USA",
                "tags": [
                    {"type": "instrument", "value": "AAPL", "threshold": 0.6}
                ]
            },
            {
                "id": "126",
                "title": "Tech in the USA",
                "content": "Content about tech in the USA",
                "tags": [
                    {"type": "country", "value": "USA", "threshold": 0.4}
                ]
            },
            {
                "id": "127",
                "title": "Tech in the UK",
                "content": "Content about tech in the UK",
                "tags": [
                    {"type": "country", "value": "UK", "threshold": 0.5}
                ]
            }
        ]

        suggestions = get_alternative_suggestions(users, content)
        self.assertEqual(len(suggestions), 1)
        self.assertEqual(suggestions[0]['user'], 'Jane Doe')
        self.assertEqual(len(suggestions[0]['suggestions']), 2)
        self.assertEqual(suggestions[0]['suggestions'][0]['type'], 'instrument')
        self.assertEqual(suggestions[0]['suggestions'][0]['values'], ['AAPL'])
        self.assertEqual(suggestions[0]['suggestions'][1]['type'], 'country')
        self.assertEqual(sorted(suggestions[0]['suggestions'][1]['values']), ['UK', 'USA'])

if __name__ == '__main__':
    unittest.main()
