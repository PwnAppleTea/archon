"""
send balance report to email
"""

import sys

import archon.exchange.exchanges as exc
import archon.broker as broker
import archon.arch as arch
import archon.plugins.mail as mail

import json
import requests
from jinja2 import Template
import jinja2
import pickle

abroker = broker.Broker()
arch.setClientsFromFile(abroker)
a = arch.Arch()
ae = [exc.KUCOIN, exc.BITTREX, exc.CRYPTOPIA, exc.KRAKEN, exc.BINANCE, exc.HITBTC]
a.set_active_exchanges(ae)

def sort_usd(d):
    d = sorted(d, key=lambda k: k['USDvalue'])
    d.reverse()   
    return d

def process(bl):
    newbl = list()    
    for x in bl:
        x['USDvalue'] = round(x['USDvalue'],2)
        if x['USDvalue'] > 1:
            newbl.append(x)
    newbl = sort_usd(newbl)
    return newbl

def write_to_file(html):
    #print (total_all)
    date_broker_format = "%Y-%m-%d"
    from datetime import datetime
    ds = datetime.now().strftime("%Y%m%d")
    fn = '$HOME/balance_report' + ds + '.html'
    with open(fn,'w') as f:
        f.write(html)

def per_exchange(bl, e):
    l = list(filter(lambda x: x['exchange']==e,bl))
    per_exchange = round(sum([float(x['USDvalue']) for x in l]),2)
    return per_exchange


def balance_report():
    bl = a.global_balances()
    bl = process(bl)

    total_all = 0

    for x in bl:
        total_all += x['USDvalue']

    total_all = round(total_all,2)

    exc = list(set([x['exchange'] for x in bl]))
    per = list()
    for e in exc:
        x = per_exchange(bl,e)
        per.append({"exchange": e,"USDvalue":x})

    per = sort_usd(per)

    loader = jinja2.FileSystemLoader('./balances.html')
    env = jinja2.Environment(loader=loader)
    template = env.get_template('')
    html = template.render(balances=bl,per=per,total=total_all)
    write_to_file(html)
    #mail.send_mail_html(abroker, "Balance Report", html)

if __name__=='__main__':
    balance_report()
    