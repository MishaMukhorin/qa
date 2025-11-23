import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from currency_converter import CurrencyConverter


class TestCurrencyConverter:

    @pytest.fixture
    def converter(self):
        return CurrencyConverter()

    @pytest.fixture
    def mock_response(self):
        mock = Mock()
        mock.status_code = 200
        mock.json.return_value = {"rate": 1.2}
        return mock

    def test_init_default_values(self):
        converter = CurrencyConverter()
        assert converter.api_url == "http://localhost:3000"
        assert converter.cache == {}
        assert converter.conversion_history == []

    def test_init_custom_url(self):
        converter = CurrencyConverter("http://custom.url")
        assert converter.api_url == "http://custom.url"

    @patch('currency_converter.requests.get')
    def test_get_exchange_rate_success(self, mock_get, converter, mock_response):
        mock_get.return_value = mock_response
        rate = converter.get_exchange_rate("USD", "EUR")
        assert rate == 1.2
        mock_get.assert_called_once_with("http://localhost:3000/rate/USD/EUR")

    @patch('currency_converter.requests.get')
    def test_get_exchange_rate_failure(self, mock_get, converter):
        mock_get.return_value.status_code = 404
        with pytest.raises(ValueError, match="Failed to fetch rate"):
            converter.get_exchange_rate("USD", "EUR")

    @patch('currency_converter.requests.get')
    def test_get_exchange_rate_uses_cache(self, mock_get, converter, mock_response):
        mock_get.return_value = mock_response
        rate1 = converter.get_exchange_rate("USD", "EUR")
        rate2 = converter.get_exchange_rate("USD", "EUR")
        assert rate1 == rate2
        mock_get.assert_called_once()

    @patch('currency_converter.requests.get')
    def test_convert_positive_amount(self, mock_get, converter, mock_response):
        mock_get.return_value = mock_response
        result = converter.convert(100, "USD", "EUR")
        assert result == 120.0

    def test_convert_negative_amount(self, converter):
        with pytest.raises(ValueError, match="Amount cannot be negative"):
            converter.convert(-100, "USD", "EUR")

    def test_convert_same_currency(self, converter):
        result = converter.convert(100, "USD", "USD")
        assert result == 100

    @patch('currency_converter.requests.get')
    def test_convert_adds_to_history(self, mock_get, converter, mock_response):
        mock_get.return_value = mock_response
        converter.convert(100, "USD", "EUR")
        assert len(converter.conversion_history) == 1
        assert converter.conversion_history[0]["amount"] == 100
        assert converter.conversion_history[0]["from"] == "USD"
        assert converter.conversion_history[0]["to"] == "EUR"
        assert converter.conversion_history[0]["result"] == 120.0

    @patch('currency_converter.requests.get')
    def test_convert_multiple(self, mock_get, converter, mock_response):
        mock_get.return_value = mock_response
        results = converter.convert_multiple([100, 200, 300], "USD", "EUR")
        assert results == [120.0, 240.0, 360.0]

    def test_get_conversion_history(self, converter):
        converter.conversion_history = [{"test": "data"}]
        history = converter.get_conversion_history()
        assert history == [{"test": "data"}]
        history.append({"new": "item"})
        assert len(converter.conversion_history) == 1

    @patch('currency_converter.requests.get')
    def test_clear_history(self, mock_get, converter, mock_response):
        mock_get.return_value = mock_response
        converter.convert(100, "USD", "EUR")
        assert len(converter.conversion_history) == 1
        converter.clear_history()
        assert len(converter.conversion_history) == 0

    @patch('currency_converter.requests.get')
    def test_clear_cache(self, mock_get, converter, mock_response):
        mock_get.return_value = mock_response
        converter.get_exchange_rate("USD", "EUR")
        assert len(converter.cache) == 1
        converter.clear_cache()
        assert len(converter.cache) == 0
        assert len(converter.cache_expiry) == 0

    @patch('currency_converter.requests.get')
    def test_calculate_profit_positive(self, mock_get, converter, mock_response):
        mock_get.return_value = mock_response
        profit = converter.calculate_profit(100, "USD", "EUR", 150)
        assert profit == 30.0

    @patch('currency_converter.requests.get')
    def test_calculate_profit_negative(self, mock_get, converter, mock_response):
        mock_get.return_value = mock_response
        profit = converter.calculate_profit(100, "USD", "EUR", 100)
        assert profit == -20.0

    @patch('currency_converter.requests.get')
    def test_get_best_rate(self, mock_get, converter):
        def mock_response_factory(rate):
            mock = Mock()
            mock.status_code = 200
            mock.json.return_value = {"rate": rate}
            return mock

        mock_get.side_effect = [
            mock_response_factory(1.2),
            mock_response_factory(1.5),
            mock_response_factory(1.1)
        ]

        best = converter.get_best_rate("USD", ["EUR", "GBP", "JPY"])
        assert best == ("GBP", 1.5)

    @patch('currency_converter.requests.get')
    def test_get_best_rate_no_valid_rates(self, mock_get, converter):
        mock_get.side_effect = Exception("API Error")
        with pytest.raises(ValueError, match="No valid rates found"):
            converter.get_best_rate("USD", ["EUR"])

    def test_is_cache_valid_not_in_cache(self, converter):
        assert not converter._is_cache_valid("test_key")

    def test_is_cache_valid_no_expiry(self, converter):
        converter.cache["test_key"] = 1.2
        assert not converter._is_cache_valid("test_key")

    def test_is_cache_valid_expired(self, converter):
        converter.cache["test_key"] = 1.2
        converter.cache_expiry["test_key"] = datetime.now() - timedelta(hours=2)
        assert not converter._is_cache_valid("test_key")

    def test_is_cache_valid_not_expired(self, converter):
        converter.cache["test_key"] = 1.2
        converter.cache_expiry["test_key"] = datetime.now() + timedelta(hours=1)
        assert converter._is_cache_valid("test_key")

    def test_update_cache(self, converter):
        converter._update_cache("test_key", 1.5)
        assert converter.cache["test_key"] == 1.5
        assert "test_key" in converter.cache_expiry
        assert converter.cache_expiry["test_key"] > datetime.now()

    @patch('currency_converter.requests.get')
    def test_add_to_history(self, mock_get, converter, mock_response):
        mock_get.return_value = mock_response
        converter.convert(100, "USD", "EUR")
        history = converter.conversion_history[0]
        assert "timestamp" in history
        assert history["amount"] == 100
        assert history["from"] == "USD"
        assert history["to"] == "EUR"
        assert history["result"] == 120.0

    @patch('currency_converter.requests.get')
    def test_convert_rounding(self, mock_get, converter):
        mock = Mock()
        mock.status_code = 200
        mock.json.return_value = {"rate": 1.234567}
        mock_get.return_value = mock
        result = converter.convert(100, "USD", "EUR")
        assert result == 123.46

    @patch('currency_converter.requests.get')
    def test_cache_expiry_duration(self, mock_get, converter, mock_response):
        mock_get.return_value = mock_response
        converter.get_exchange_rate("USD", "EUR")
        cache_key = "USD_EUR"
        expiry_time = converter.cache_expiry[cache_key]
        time_diff = expiry_time - datetime.now()
        assert timedelta(minutes=59) < time_diff < timedelta(minutes=61)