from unittest.mock import Mock, patch

import pytest
import requests
from bs4 import BeautifulSoup

from currency_scraper.scraper import NbpCurrencyScrapper


@pytest.fixture
def scraper_fix():
    scraper = NbpCurrencyScrapper()
    yield scraper
    del scraper


@pytest.fixture
def page_fix():
    return '<a href="/test">test</a>'


class TestNbpCurrencyScrapper:
    @patch.object(requests, 'get')
    def test_get_page(self, mock_get, scraper_fix):
        mock_response = Mock()
        mock_get.return_value = mock_response
        mock_response.content = 'mock return'
        result = scraper_fix._get_page(url='test', parser='lxml')
        assert 'mock return' in result.string

    def test_get_absolute_url_from_href(self, scraper_fix, page_fix):
        result = scraper_fix._get_absolute_url_from_href(
            soup=BeautifulSoup(page_fix, 'lxml'), pattern='test'
        )
        assert result == 'https://www.nbp.pl/test'
