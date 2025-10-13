from unittest.mock import Mock

import pytest


@pytest.fixture
def mock_github_app_lib():
    """Builds new mock Instance of GithubAppLib"""
    github_app_lib = Mock()
    github_app_lib.settings = Mock()
    github_app_lib.create_jwt = Mock(return_value="mock_jwt_token")

    return github_app_lib
