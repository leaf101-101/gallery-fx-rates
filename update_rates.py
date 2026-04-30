import requests
import json
import os
from datetime import datetime

API_KEY = os.environ.get('EXCHANGERATE_API_KEY')

GALLERY_RATE_FACTOR = 0.98
TARGET_CURRENCIES = {
    'USD': 'USD/ZAR',
    'EUR': 'EUR/ZAR',
    'GBP': 'GBP/ZAR',
    'AUD': 'AUD/ZAR',
    'CHF': 'CHF/ZAR',
}

def get_rates():
    url = "https://v6.exchangerate-api.com/v6/" + API_KEY + "/latest/ZAR"
    data = requests.get(url, timeout=15).json()
    print("API result:", data.get('result'))
    rates = {}
    today = datetime.now().strftime('%Y-%m-%d')
    for code, pair in TARGET_CURRENCIES.items():
        zar_per_foreign = round(1 / data['conversion_rates'][code], 6)
        rates[code] = {
            'pair': pair,
            'gallery_rate': round(zar_per_foreign * GALLERY_RATE_FACTOR, 4),
            'date': today
        }
    return rates

rates = get_rates()
with open('current_rates.json', 'w') as f:
    json.dump(rates, f, indent=2)
print('Rates saved.')
