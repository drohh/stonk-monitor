import datetime
from typing import Any, Dict, List, Optional
import finnhub
from config import API_KEY


def get_utc_from_unix_time(unix_ts: Optional[Any]) -> Optional[datetime.datetime]:
    return datetime.datetime.fromtimestamp(int(unix_ts), tz=datetime.timezone.utc)
    

def get_exchange_data(symbols) -> List[Dict[str, Any]]:
    finnhub_client = finnhub.Client(api_key=API_KEY)
    data = []
    for symbol in symbols:
        data.append(finnhub_client.quote(symbol))
    return data

def _get_exchange_insert_query() -> str:
    return '''
    INSERT INTO bitcoin.exchange (
        id,
        name,
        rank,
        percenttotalvolume,
        volumeusd,
        tradingpairs,
        socket,
        exchangeurl,
        updated_unix_millis,
        updated_utc
    )
    VALUES (
        %(exchangeId)s,
        %(name)s,
        %(rank)s,
        %(percentTotalVolume)s,
        %(volumeUsd)s,
        %(tradingPairs)s,
        %(socket)s,
        %(exchangeUrl)s,
        %(updated)s,
        %(update_dt)s
    );
    '''

def run() -> None:
    data = get_exchange_data()
    for d in data:
        d['update_dt'] = get_utc_from_unix_time(d.get('updated'))
    with WarehouseConnection(get_warehouse_creds()).managed_cursor() as curr:
        p.execute_batch(curr, _get_exchange_insert_query(), data)

if __name__ == '__main__':
    symbols = ['AMC','GME']
    fmt = "%m-%d-%Y %H:%M:%S%z"
    data = get_exchange_data(symbols)
    print(data)

    # convert dt for the first ticker provided, and add an updated_dt key
    dt = data[0].get('t')
    data[0]['updated_dt'] = get_utc_from_unix_time(dt)

    print(data)
