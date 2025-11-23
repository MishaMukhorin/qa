import requests
from datetime import datetime, timedelta

class CurrencyConverter:
    def __init__(self, api_url="http://localhost:3000"):
        self.api_url = api_url
        self.cache = {}
        self.cache_expiry = {}
        self.cache_duration = timedelta(hours=1)
        self.conversion_history = []
    
    def get_exchange_rate(self, from_currency, to_currency):
        cache_key = f"{from_currency}_{to_currency}"
        
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        response = requests.get(f"{self.api_url}/rate/{from_currency}/{to_currency}")
        
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch rate: {response.status_code}")
        
        rate = response.json()["rate"]
        self._update_cache(cache_key, rate)
        return rate
    
    def convert(self, amount, from_currency, to_currency):
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        
        if from_currency == to_currency:
            return amount
        
        rate = self.get_exchange_rate(from_currency, to_currency)
        result = amount * rate
        
        self._add_to_history(amount, from_currency, to_currency, result)
        return round(result, 2)
    
    def convert_multiple(self, amounts, from_currency, to_currency):
        return [self.convert(amt, from_currency, to_currency) for amt in amounts]
    
    def get_conversion_history(self):
        return self.conversion_history.copy()
    
    def clear_history(self):
        self.conversion_history = []
    
    def clear_cache(self):
        self.cache = {}
        self.cache_expiry = {}
    
    def calculate_profit(self, buy_amount, buy_currency, sell_currency, sell_price):
        converted = self.convert(buy_amount, buy_currency, sell_currency)
        profit = sell_price - converted
        return round(profit, 2)
    
    def get_best_rate(self, from_currency, target_currencies):
        rates = {}
        for currency in target_currencies:
            try:
                rates[currency] = self.get_exchange_rate(from_currency, currency)
            except:
                continue
        
        if not rates:
            raise ValueError("No valid rates found")
        
        return max(rates.items(), key=lambda x: x[1])
    
    def _is_cache_valid(self, cache_key):
        if cache_key not in self.cache:
            return False
        
        if cache_key not in self.cache_expiry:
            return False
        
        return datetime.now() < self.cache_expiry[cache_key]
    
    def _update_cache(self, cache_key, rate):
        self.cache[cache_key] = rate
        self.cache_expiry[cache_key] = datetime.now() + self.cache_duration
    
    def _add_to_history(self, amount, from_currency, to_currency, result):
        self.conversion_history.append({
            "timestamp": datetime.now().isoformat(),
            "amount": amount,
            "from": from_currency,
            "to": to_currency,
            "result": result
        })