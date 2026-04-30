"""
Fine Art Portfolio — Daily FX Rate Fetcher
Uses ExchangeRate-API (exchangerate-api.com) for reliable rates
Gallery rate = 98% of mid-market rate
"""
import requests
from datetime import datetime
import json

# ============================================================
# CONFIGURATION — Paste your API key here
# ============================================================
API_KEY = "b8088bd0beb33ff56c9dafdb"
# ============================================================

BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/ZAR"

GALLERY_RATE_FACTOR = 0.98  # 98% of mid-market rate

TARGET_CURRENCIES = {
    'USD': 'USD/ZAR',
    'EUR': 'EUR/ZAR',
    'GBP': 'GBP/ZAR',
    'AUD': 'AUD/ZAR',
    'CHF': 'CHF/ZAR',
}

def fetch_rates():
    """Fetch latest rates from ExchangeRate-API with ZAR as base"""
    try:
        response = requests.get(BASE_URL, timeout=15)
        response.raise_for_status()
        data = response.json()
        if data.get('result') != 'success':
            raise RuntimeError(f"API error: {data.get('error-type', 'unknown')}")
        return data
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch rates: {e}")

def calculate_gallery_rates(api_data):
    """
    API returns: 1 ZAR = X foreign units
    We need:     1 foreign unit = Y ZAR  →  Y = 1 / X
    Then apply 98% factor.
    """
    conversion_rates = api_data['conversion_rates']
    today = datetime.now().strftime('%Y-%m-%d')
    gallery_rates = {}

    for currency_code, pair_label in TARGET_CURRENCIES.items():
        if currency_code not in conversion_rates:
            print(f"Warning: {currency_code} not found in API response, skipping.")
            continue

        zar_per_foreign = round(1 / conversion_rates[currency_code], 6)
        gallery_rate = round(zar_per_foreign * GALLERY_RATE_FACTOR, 4)

        gallery_rates[currency_code] = {
            'pair': pair_label,
            'mid_market_rate': zar_per_foreign,
            'gallery_rate': gallery_rate,
            'factor': GALLERY_RATE_FACTOR,
            'date': today,
        }

    return gallery_rates

def get_rates():
    """Main entry point: fetch and return gallery rates"""
    api_data = fetch_rates()
    gallery_rates = calculate_gallery_rates(api_data)
    return gallery_rates

if __name__ == '__main__':
    rates = get_rates()
    print(f"\nFine Art Portfolio — Exchange Rates ({datetime.now().strftime('%d %B %Y')})\n")
    print(f"{'Pair':<12} {'Mid-market':>12} {'Gallery rate (98%)':>20}")
    print("-" * 46)
    for code, data in rates.items():
        print(f"{data['pair']:<12} {data['mid_market_rate']:>12.4f} {data['gallery_rate']:>20.4f}")
    print()
