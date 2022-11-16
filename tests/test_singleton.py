from dataclasses import dataclass

import pytest

from currency_scraper.singleton import Singleton


@dataclass
class UserSingletonTest(metaclass=Singleton):
    name: str
    surname: str


@pytest.fixture
def first_user_fix():
    first_user = UserSingletonTest('Test', 'User')
    yield first_user
    del first_user
    Singleton._instances.clear()


def test_singleton(first_user_fix):
    second_user = UserSingletonTest('Test2', 'User2')
    assert first_user_fix is second_user
    del second_user
    Singleton._instances.clear()
