from unittest import TestCase
from unittest.mock import Mock, patch

from src.api_client.search import search_beatmap


class TestApiClient(TestCase):
    @patch('requests.get')
    def test_search_beatmap(self, mock_requests_get):
        # Arrange
        expected_result = [
            ("Title 1", "Artist 1", "Difficulty 1", "SetId 1"),
            ("Title 2", "Artist 2", "Difficulty 2", "SetId 2")
        ]
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": [
                {"Title": "Title 1", "Artist": "Artist 1", "ChildrenBeatmaps": [{"DiffName": "Difficulty 1"}],
                 "SetId": "SetId 1"},
                {"Title": "Title 2", "Artist": "Artist 2", "ChildrenBeatmaps": [{"DiffName": "Difficulty 2"}],
                 "SetId": "SetId 2"}
            ]
        }
        mock_requests_get.return_value = mock_response

        # Act
        result = search_beatmap("query")

        # Assert
        self.assertEqual(result, expected_result)

    @patch('requests.get')
    def test_search_beatmap_raises_error_on_empty_api_response(self, mock_requests_get):
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_requests_get.return_value = mock_response

        # Act & Assert
        with self.assertRaises(ValueError):
            search_beatmap("query")

    @patch('requests.get')
    def test_search_beatmap_raises_error_on_invalid_api_response_structure(self, mock_requests_get):
        mock_response = Mock()
        mock_response.json.return_value = {"invalid_key": []}
        mock_requests_get.return_value = mock_response

        # Act & Assert
        with self.assertRaises(ValueError):
            search_beatmap("query")