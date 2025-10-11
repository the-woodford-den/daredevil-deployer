"""GithubAppLib tests configs/github_app_lib.py"""


class TestGithubAppLib:
    """test suite --> GithubAppLib"""

    def test_create_jwt(self, mock_github_app_lib):
        """Test create_jwt is called with the correct client_id"""
        c_id = "1234"
        result = mock_github_app_lib.create_jwt(c_id)

        mock_github_app_lib.create_jwt.assert_called_once_with(c_id)
        assert result == "mock_jwt_token"
