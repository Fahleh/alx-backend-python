#!/usr/bin/env python3
'''Module to test utils file
'''
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch


class TestAccessNestedMap(unittest.TestCase):
    """class for testing access_nestd_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {'b': 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that the method returns accuately"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b')
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """ Test that KeyErrors are raised accutately."""
        with self.assertRaises(KeyError) as keyErr:
            access_nested_map(nested_map, path)
        self.assertEqual(f"KeyError('{expected}')", repr(keyErr.exception))


class TestGetJson(unittest.TestCase):
    """Class for Testing GetJson"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """
        Test for the utils.get_json function to checkthat it
        returns the expected result
        """
        set_up = {'return_value.json.return_value': test_payload}
        builder = patch('requests.get', **set_up)
        fakeAPI = builder.start()
        self.assertEqual(get_json(test_url), test_payload)
        fakeAPI.assert_called_once()
        builder.stop()


class TestMemoize(unittest.TestCase):
    """Class to test utils.memoize"""

    def test_memoize(self):
        """
        Tests that a functionn called twice within a short period returns
        executes once but the right data twice.
        """

        class TestClass:
            """Test Class for wrapping memoize """

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as fakeCall:
            test_class = TestClass()
            test_class.a_property()
            test_class.a_property()
            fakeCall.assert_called_once()
