from pathlib import Path
from unittest import TestCase

from src.noosu.parse_beatmap import parse_general


class TestParseGeneral(TestCase):
    def test_parse_general_valid_content(self):
        content = """
AudioFilename: audio.mp3
AudioLeadIn: 1000
PreviewTime: 5000
        """
        src_dir_path = Path("/path/to/src_dir")
        result = parse_general(content, src_dir_path)
        expected_result = {
            "AudioFilename": Path("/path/to/src_dir/audio.mp3"),
            "AudioLeadIn": 1000,
            "PreviewTime": 5000
        }
        self.assertEqual(result, expected_result)


    def test_parse_general_negative_preview_time(self):
        content = """
AudioFilename: audio.mp3
AudioLeadIn: 0
PreviewTime: -100
        """
        src_dir_path = Path("/path/to/src_dir")
        result = parse_general(content, src_dir_path)
        expected_result = {
            "AudioFilename": Path("/path/to/src_dir/audio.mp3"),
            "AudioLeadIn": 0,
            "PreviewTime": 0  # PreviewTime should be set to 0 if negative
        }
        self.assertEqual(result, expected_result)

