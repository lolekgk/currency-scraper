from datetime import date, datetime
from unittest.mock import MagicMock, Mock, patch

import pytest

from currency_scraper.database import Database
from currency_scraper.models import Currency


@pytest.fixture
def usd_currency():
    usd = Currency(
        currency_code='USD',
        currency_name='dolar',
        convertion_rate=1,
        currency_avg_rate=4.5,
        date=datetime(2022, 10, 10),
    )
    yield usd
    del usd


@pytest.fixture
def eur_currency():
    eur = Currency(
        currency_code='EUR',
        currency_name='euro',
        convertion_rate=1,
        currency_avg_rate=4.48,
        date=datetime(2022, 10, 10),
    )
    yield eur
    del eur


@pytest.fixture
def expected_usd_result_fix():
    usd = [
        ('currency_code', 'USD'),
        ('currency_name', 'dolar'),
        ('convertion_rate', 1),
        ('currency_avg_rate', 4.5),
        ('date', datetime(2022, 10, 10, 0, 0)),
    ]
    yield usd
    del usd


@pytest.fixture
def date_fix():
    test_date = date(2022, 10, 10)
    yield test_date
    del test_date


@pytest.fixture
def mocked_db_data_fix(usd_currency, eur_currency):
    mocked_db_data = [usd_currency, eur_currency]
    yield mocked_db_data
    del mocked_db_data


@pytest.fixture
def mocked_database_fix(mocked_db_data_fix):
    with patch("currency_scraper.database.MongoClient") as mocked_database:
        database_instance = MagicMock()
        database_instance.__getitem__.return_value.__getitem__.return_value = (
            mocked_db_data_fix
        )
        mocked_database.return_value = database_instance
        yield mocked_database


class TestDatabase:
    def test_database_init(self, mocked_database_fix, mocked_db_data_fix):
        database_object = Database()
        assert database_object.currency_collections == mocked_db_data_fix

    def test_get_date_filter(self, mocked_database_fix, date_fix):
        database_object = Database()
        result = database_object._get_date_filter(date_fix)
        assert result == {
            'date': {
                '$gte': date_fix,
                '$lte': date_fix,
            }
        }

    def test_get_currency_filter_with_lowercase_code(
        self, mocked_database_fix
    ):
        database_object = Database()
        result = database_object._get_currency_filter(currency_code='abc')
        assert result == {'currency_code': 'ABC'}

    def test_get_currency_filter_with_upperrcase_code(
        self, mocked_database_fix
    ):
        database_object = Database()
        result = database_object._get_currency_filter(currency_code='ABC')
        assert result == {'currency_code': 'ABC'}

    def test_get_all_currencies(
        self, mocked_database_fix, usd_currency, expected_usd_result_fix
    ):
        database_object = Database()
        mocked_collection = Mock()
        mocked_collection.find.return_value.sort.return_value = usd_currency

        database_object.currency_collections = mocked_collection
        result = database_object.get_all_currencies()
        assert result == expected_usd_result_fix

    def test_get_currency_from_all_dates(
        self, mocked_database_fix, usd_currency, expected_usd_result_fix
    ):
        database_object = Database()
        mocked_collection = Mock()
        mocked_collection.find.return_value.sort.return_value = usd_currency
        database_object.currency_collections = mocked_collection
        database_object._get_currency_filter.return_value = 'tests'
        result = database_object.get_currency_from_all_dates(
            currency_code='USD'
        )
        assert result == expected_usd_result_fix

    def test_get_currnect_from_provided_date(
        self, mocked_database_fix, date_fix, eur_currency
    ):
        database_object = Database()
        database_object._get_date_filter.return_value = 'mocked'
        database_object._get_currency_filter.return_value = 'mocked'
        mocked_collection = Mock()
        mocked_collection.find_one.return_value = eur_currency
        database_object.currency_collections = mocked_collection
        result = database_object.get_currency_from_provided_date(
            currency_code='eur', date=date_fix
        )
        assert result == eur_currency

    def test_is_date_in_database_with_no_date(
        self, mocked_database_fix, date_fix
    ):
        database_object = Database()
        database_object._get_date_filter.return_value = 'mocked'
        mocked_collection = Mock()
        mocked_collection.find_one.return_value = None
        database_object.currency_collections = mocked_collection
        result = database_object.is_date_in_database(date_fix)
        assert result is False

    def test_is_date_in_database_with_date(
        self, mocked_database_fix, date_fix
    ):
        database_object = Database()
        database_object._get_date_filter.return_value = 'mocked'
        mocked_collection = Mock()
        mocked_collection.find_one.return_value = date_fix
        database_object.currency_collections = mocked_collection
        result = database_object.is_date_in_database(date_fix)
        assert result is True

    def test_insert_currencies(self, mocked_database_fix, mocked_db_data_fix):
        database_object = Database()
        mocked_collection = Mock()
        mocked_collection.insert_many.return_value = mocked_db_data_fix
        database_object.currency_collections = mocked_collection
        result = database_object.insert_currencies(mocked_db_data_fix)
        assert result == mocked_db_data_fix
