import archon.exchange.exchanges as exc
import archon.broker as broker
import archon.feeds.cryptocompare as cryptocompare

a = broker.Broker()
a.set_keys_exchange_file()


ae = [exc.KUCOIN, exc.BITTREX, exc.CRYPTOPIA, exc.HITBTC, exc.BINANCE]
a.set_active_exchanges(ae)

ms = a.fetch_global_markets()
print (len(ms))

ms2 = list(filter(lambda x: x['denom'] == 'BTC', ms))
print (len(ms2))

for x in ms2:
    print (x)

print ("markets per exchange")
exs = list(set([x['exchange'] for x in ms]))
for e in exs:
    z = list(filter(lambda t: t['exchange']==e, ms))
    print (e,len(z))

"""
markets per exchange
Bittrex 292
Kucoin 402
Cryptopia 1562
Binance 414
Hitbtc 911
"""

