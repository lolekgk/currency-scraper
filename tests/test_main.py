from datetime import date, datetime
from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from currency_scraper.main import app
from currency_scraper.models import UserFriendlyCurrency

client = TestClient(app)


@pytest.fixture
def currency_usd_fix():
    test_currency_usd = UserFriendlyCurrency(
        currency_code='USD',
        currency_name='dolar',
        convertion_rate=1,
        currency_avg_rate=4.5,
        date=date(2022, 10, 10),
    )
    yield test_currency_usd
    del test_currency_usd


@pytest.fixture
def currency_usd_2_fix():
    test_currency_usd_2 = UserFriendlyCurrency(
        currency_code='USD',
        currency_name='dolar',
        convertion_rate=1,
        currency_avg_rate=4.52,
        date=date(2022, 12, 10),
    )
    yield test_currency_usd_2
    del test_currency_usd_2


@pytest.fixture
def currency_eur_fix():
    test_currency_eur = UserFriendlyCurrency(
        currency_code='EUR',
        currency_name='euro',
        convertion_rate=1,
        currency_avg_rate=4.82,
        date=date(2022, 9, 10),
    )
    yield test_currency_eur
    del test_currency_eur


@pytest.fixture
def all_currencies_expected_result_fix():
    result = [
        {
            "currency_code": "USD",
            "currency_name": "dolar",
            "convertion_rate": 1,
            "currency_avg_rate": 4.52,
            "date": "2022-12-10",
        },
        {
            "currency_code": "USD",
            "currency_name": "dolar",
            "convertion_rate": 1,
            "currency_avg_rate": 4.5,
            "date": "2022-10-10",
        },
        {
            "currency_code": "EUR",
            "currency_name": "euro",
            "convertion_rate": 1,
            "currency_avg_rate": 4.82,
            "date": "2022-09-10",
        },
    ]
    yield result
    del result


@pytest.fixture
def mocked_database_fix(
    currency_usd_fix, currency_usd_2_fix, currency_eur_fix
):
    with patch('currency_scraper.main.Database') as mocked_database:
        database_instance = Mock()
        database_instance.get_all_currencies.return_value = [
            currency_usd_2_fix,
            currency_usd_fix,
            currency_eur_fix,
        ]
        database_instance.get_currency_from_provided_date.return_value = (
            currency_usd_fix
        )
        database_instance.get_currency_from_all_dates.return_value = [
            currency_usd_fix,
            currency_usd_2_fix,
        ]
        database_instance.is_date_in_database.return_value = None
        database_instance.insert_currencies.return_value = [
            currency_usd_2_fix,
            currency_usd_fix,
            currency_eur_fix,
        ]
        mocked_database.return_value = database_instance
        yield mocked_database


@pytest.fixture
def mocked_scraper_fix():
    with patch('currency_scraper.main.NbpCurrencyScrapper') as mocked_scraper:
        scraper_instance = Mock()
        scraper_instance.scrap_publication_date.return_value = datetime(
            2022, 10, 10
        )
        scraper_instance.scrap_currencies.return_value = 'test'
        mocked_scraper.return_value = scraper_instance
        yield mocked_scraper


@pytest.fixture
def failure_prone_mocked_database_fix():
    with patch('currency_scraper.main.Database') as mocked_database:
        database_instance = Mock()
        database_instance.get_all_currencies.return_value = []
        database_instance.get_currency_from_all_dates.return_value = []
        database_instance.get_currency_from_provided_date.return_value = None
        database_instance.is_date_in_database.return_value = True
        mocked_database.return_value = database_instance
        yield mocked_database


class TestMain:
    def test_get_all_currencies(
        self, mocked_database_fix, all_currencies_expected_result_fix
    ):
        response = client.get('/currencies')
        assert response.status_code == 200
        assert response.json() == all_currencies_expected_result_fix

    def test_get_all_currencies_with_empty_database(
        self,
        failure_prone_mocked_database_fix,
    ):
        response = client.get('currencies')
        expected_result = {
            "detail": "Database is empty, please add some data."
        }
        assert response.status_code == 404
        assert response.json() == expected_result

    def test_get_currency(self, mocked_database_fix):
        response = client.get("/currencies/usd")
        expected_result = [
            {
                "currency_code": "USD",
                "currency_name": "dolar",
                "convertion_rate": 1,
                "currency_avg_rate": 4.5,
                "date": "2022-10-10",
            },
            {
                "currency_code": "USD",
                "currency_name": "dolar",
                "convertion_rate": 1,
                "currency_avg_rate": 4.52,
                "date": "2022-12-10",
            },
        ]
        assert response.status_code == 200
        assert response.json() == expected_result

    def test_get_currency_with_query_parameter(self, mocked_database_fix):
        response = client.get("/currencies/usd?date=2022-10-10")
        expected_result = {
            "currency_code": "USD",
            "currency_name": "dolar",
            "convertion_rate": 1,
            "currency_avg_rate": 4.5,
            "date": "2022-10-10",
        }
        assert response.status_code == 200
        assert response.json() == expected_result

    def test_get_inexistent_currency(self, failure_prone_mocked_database_fix):
        response = client.get("/currencies/gbp")
        expected_result = {"detail": "Currency not found in database."}
        assert response.status_code == 404
        assert response.json() == expected_result

    def test_get_inexistent_currency_with_query_parameter(
        self,
        failure_prone_mocked_database_fix,
    ):
        response = client.get("/currencies/gbp?date=2022-10-10")
        expected_result = {"detail": "Currency not found in database."}
        assert response.status_code == 404
        assert response.json() == expected_result

    def test_add_currencies(
        self,
        mocked_database_fix,
        mocked_scraper_fix,
        all_currencies_expected_result_fix,
    ):
        response = client.post("/currencies")
        assert response.status_code == 201
        assert response.json() == all_currencies_expected_result_fix

    def test_insert_existing_currencies(
        self, failure_prone_mocked_database_fix, mocked_scraper_fix
    ):
        response = client.post("/currencies")
        expected_result = {
            "detail": "Currencies publicated on: '2022-10-10' already exists in database."
        }
        assert response.status_code == 409
        assert response.json() == expected_result
