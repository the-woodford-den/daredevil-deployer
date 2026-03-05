from unittest.mock import Mock

import pytest


@pytest.fixture
def mock_git_lib():
    """Builds new mock Instance of GithubAppLib"""
    git_lib = Mock()
    git_lib.settings = Mock()
    git_lib.create_jwt = Mock(return_value="mock_jwt_token")

    return git_lib
