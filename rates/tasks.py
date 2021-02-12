from celery import shared_task
import redis
import requests
import re
from decimal import Decimal
from django.core.cache import cache
import ccxt

FIATS_TO_FETCH = ('USD','EUR',)
CRYPTOS_TO_FETCH = ('BTC','ETH',)

@shared_task
def fetch_ecb_rates():
    from models import FiatCurrency, FiatRate
    r = requests.get("https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml")

    r_s = r'<Cube currency=\'(\w+)\' rate=\'(\d+\.+\d+)\''

    base_currency = FiatCurrency.objects.update_or_create(symbol="EUR", defaults={'in_EUR': Decimal(1)})

    for r_match in re.finditer(r_s, r.text):
        symbol = r_match.group(1)
        rate = Decimal(r_match.group(2))
        target_currency = FiatCurrency.objects.update_or_create(symbol=symbol, defaults={'in_EUR': rate})
        FiatRate.objects.create(base=base_currency, target=target_currency, rate=rate)
        # no expiry
        cache.set("fx_"+symbol+"_in_EUR", rate, None)


@shared_task
def fetch_bitstamp():
    public_client = bitstamp.client.Public()

    base_currency = FiatCurrency.objects.get(symbol="USD")

    for crypto in CRYPTOS_TO_FETCH:
        ticker = public_client.ticker(crypto)
        symbol = crypto
        rate = Decimal(ticker['last'])
        CryptoRateHistory.create(base=base_currency, target=target_crypto, rate=rate)
        cache.set("fx_"+symbol+"_in_USD", rate, None)


@shared_task
def fetch_coinbase:
    import cbpro

    public_client = cbpro.PublicClient()

    base_currency = FiatCurrency.objects.get(symbol="USD")

    for crypto in CRYPTOS_TO_FETCH:
        ticker = public_client.get_product_ticker(product_id=crypto+'-USD')
        symbol = crypto
        rate = Decimal(ticker['last'])
        CryptoRateHistory.create(base=base_currency, target=target_crypto, rate=rate)
        cache.set("fx_"+symbol+"_in_USD", rate, None)