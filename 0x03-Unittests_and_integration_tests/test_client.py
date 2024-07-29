#!/usr/bin/env python3
""" Module for testing client """

import unittest
from unittest.mock import patch, PropertyMock, Mock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class

class TestGithubOrgClient(unittest.TestCase):
    """Class for Testing Github Org Client"""

    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch("client.get_json")
    def test_org(self, data, mock):
        """Test that the client returns the correct value"""
        url = f"https://api.github.com/orgs/{data}"
        spec = GithubOrgClient(data)
        spec.org()
        mock.assert_called_once_with(url)

    def test_public_repos_url(self):
        """
        Test that the result of _public_repos_url is the expected one
        based on the mocked payload
        """
        with patch("client.GithubOrgClient.org",
                   new_callable=PropertyMock) as mock:
            response = {"repos_url": "http://mock_url.com"}
            mock.return_value = response
            spec = GithubOrgClient("test")
            res = spec._public_repos_url
            self.assertEqual(res, response["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mocked_method):
        """
        Tests that the correct response is returned.
        Tests that the poperty andget_json were called once.
        """
        payLoad = [{"name": "Google"}, {"name": "Twitter"}]
        mocked_method.return_value = payLoad

        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mocked:

            mocked.return_value = "world"
            response = GithubOrgClient("test").public_repos()

            self.assertEqual(response, ["Google", "Twitter"])

            mocked.assert_called_once()
            mocked_method.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """unit-test for GithubOrgClient.has_license"""
        res = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(res, expected)

@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests."""
    @classmethod
    def setUpClass(cls) -> None:
        """Sets up the class fixtures before running tests."""
        payLoad = {
            "https://api.github.com/orgs/google": cls.org_payload,
            "https://api.github.com/orgs/google/repos": cls.repos_payload,
        }

        def configure(url):
            if url in payLoad:
                return Mock(**{'json.return_value': payLoad[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=configure)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Tests the public_repos method."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """Tests the public_repos method with a license."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Cleans up by removing class after all tests are run."""
        cls.get_patcher.stop()
