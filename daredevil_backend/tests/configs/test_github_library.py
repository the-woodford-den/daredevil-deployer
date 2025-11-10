"""GithubLibrary tests configs/github_library.py"""

from unittest.mock import mock_open

from utility import GitLib


class TestGitLib:
    """test suite --> GitLib"""

    def test_create_jwt(self, mocker):
        """Test create_jwt creates a JWT with the correct payload"""
        # Mock the settings
        mock_settings = mocker.MagicMock()
        mock_settings.gha_private_key = "test_key.pem"
        mocker.patch(
            "configs.github_library.get_settings", return_value=mock_settings
        )

        # Mock the file reading
        fake_private_key = b"fake_private_key_content"
        mocker.patch("builtins.open", mock_open(read_data=fake_private_key))

        # Mock jwt.encode to return a known token
        mock_jwt = "mock_jwt_token"
        mocker.patch("configs.github_library.jwt.encode", return_value=mock_jwt)

        # Mock time.time to return a consistent value
        mock_time = 1000000
        mocker.patch("configs.github_library.time.time", return_value=mock_time)

        # Create instance and call create_jwt
        github_lib = GitLib()
        result = github_lib.create_jwt(client_id="test_client_id")

        # Verify the result
        assert result == mock_jwt
