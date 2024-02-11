from unittest import TestCase

from src.noosu.parse_beatmap import extract_to_dict


class TestExtractToDict(TestCase):
    def test_extract_to_dict_empty_content(self):
        content = ""
        include_fields = ("Field1", "Field2")
        result = extract_to_dict(content, include_fields)
        self.assertEqual(result, {})

    def test_extract_to_dict_single_line(self):
        content = "Field1: Value1"
        include_fields = ("Field1",)
        result = extract_to_dict(content, include_fields)
        self.assertEqual(result, {"Field1": "Value1"})

    def test_extract_to_dict_missing_fields(self):
        content = "Field1: Value1"
        include_fields = ("Field1", "Field2")
        result = extract_to_dict(content, include_fields)
        self.assertEqual(result, {"Field1": "Value1"})

    def test_extract_to_dict_no_space_after_colon(self):
        content = "Field1:Value1\nField2:Value2"
        include_fields = ("Field1", "Field2")
        result = extract_to_dict(content, include_fields)
        self.assertEqual(result, {"Field1": "Value1", "Field2": "Value2"})


