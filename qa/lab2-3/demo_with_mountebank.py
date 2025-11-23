from currency_converter import CurrencyConverter

def demo_mountebank():
    print("=== Demo: CurrencyConverter with Mountebank Mock ===\n")
    
    converter = CurrencyConverter("http://localhost:3000")
    
    print("1. Converting 100 USD to EUR:")
    result = converter.convert(100, "USD", "EUR")
    print(f"   100 USD = {result} EUR\n")
    
    print("2. Converting 200 USD to GBP:")
    result = converter.convert(200, "USD", "GBP")
    print(f"   200 USD = {result} GBP\n")
    
    print("3. Converting 50 EUR to USD:")
    result = converter.convert(50, "EUR", "USD")
    print(f"   50 EUR = {result} USD\n")
    
    print("4. Multiple conversions:")
    results = converter.convert_multiple([100, 200, 300], "USD", "JPY")
    print(f"   [100, 200, 300] USD = {results} JPY\n")
    
    print("5. Best rate for USD among [EUR, GBP, JPY]:")
    best_currency, best_rate = converter.get_best_rate("USD", ["EUR", "GBP", "JPY"])
    print(f"   Best: {best_currency} with rate {best_rate}\n")
    
    print("6. Conversion history:")
    history = converter.get_conversion_history()
    print(f"   Total conversions: {len(history)}")
    for i, record in enumerate(history[:3], 1):
        print(f"   {i}. {record['amount']} {record['from']} -> {record['result']} {record['to']}")

if __name__ == "__main__":
    try:
        demo_mountebank()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure Mountebank is running:")
        print("  mb start --configfile mountebank_config.json")