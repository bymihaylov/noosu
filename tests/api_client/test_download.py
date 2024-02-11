from unittest import TestCase
from unittest.mock import Mock, patch, mock_open

from pygame.event import Event
from requests.exceptions import InvalidJSONError, JSONDecodeError

from src.api_client.download import download_by_set_id
from src.config import config, custom_events


class TestApiClient(TestCase):
    @patch('requests.get')
    @patch('builtins.open', new_callable=mock_open)
    @patch('pygame.event.post')
    def test_download_by_set_id_success(self, mock_post_event, mock_open_file, mock_requests_get):
        # Arrange
        set_id = '123'
        artist = 'SomeArtist'
        title = 'SomeTitle'

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'Some content'
        mock_requests_get.return_value = mock_response

        expected_event = Event(custom_events.DOWNLOAD_PACK_COMPLETED, {"set_id": set_id})

        # Act
        download_by_set_id(set_id, artist, title)

        # Assert
        filepath = config.external_packs_dir / f"{set_id} {artist} - {title}.osz"

        mock_requests_get.assert_called_once_with(f"{config.api_download_url}/{set_id}", stream=True)

        mock_open_file.assert_called_once_with(filepath, 'wb')

        mock_open_file.return_value.write.assert_called_once_with(b'Some content')

        mock_post_event.assert_called_once_with(expected_event)

    @patch('requests.get')
    @patch('builtins.print')
    def test_download_by_set_id_fail(self,mock_print, mock_requests_get):
        # Arrange
        set_id = "123"
        artist = 'SomeArtist'
        title = 'SomeTitle'

        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.content = b'Not a valid JSON content'
        mock_requests_get.return_value = mock_response

        expected_error_msg = f"JSONDecodeError"

        download_by_set_id(set_id,artist,title)

        mock_print.assert_called_with(expected_error_msg)





