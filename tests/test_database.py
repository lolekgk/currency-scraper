import pytest

from currency_scraper.database import Database
from currency_scraper.singleton import Singleton


@pytest.fixture
def database_fix():
    database = Database()
    yield database
    del database
    Singleton._instances.clear()


class TestDatabase:
    def test_is_database_singleton(self, database_fix):
        database_2 = Database()
        assert database_fix is database_2
        del database_2
        Singleton._instances.clear()
