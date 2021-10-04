import datetime
from typing import Any, Dict, List, Optional
import finnhub
from utils.finnhub_config import API_KEY
from utils.db import WarehouseConnection
from utils.psql_config import get_warehouse_creds
import psycopg2.extras as p

def get_utc_from_unix_time(unix_ts: Optional[Any]) -> Optional[datetime.datetime]:
    fmt = "%Y-%m-%d %H:%M:%S%z"
    dt = datetime.datetime.fromtimestamp(int(unix_ts), tz=datetime.timezone.utc)
    return dt.strftime(fmt)

def get_stonk_data(symbols) -> List[Dict[str, Any]]:
    finnhub_client = finnhub.Client(api_key=API_KEY)
    data = []
    for symbol in symbols:
        data.append({'symbol':symbol} | finnhub_client.quote(symbol))
    return data

def _get_stonk_insert_query() -> str:
    return '''
    INSERT INTO stonk.quotes (
        company_id,
        current_price,
        change,
        percent_change,
        day_high,
        day_low,
        open,
        previous_close,
        datetime
        )
    VALUES(
        (SELECT company_id from stonk.companies WHERE symbol=%(symbol)s),
         %(c)s,
         %(d)s,
         %(dp)s,
         %(h)s,
         %(l)s,
         %(o)s,
         %(pc)s,
         %(str_dt)s 
        );
    '''

def run() -> None:
    symbols = ['AMC','GME']
    data = get_stonk_data(symbols)
    for d in data:
        d['str_dt'] = get_utc_from_unix_time(d.get('t'))
    with WarehouseConnection(get_warehouse_creds()).managed_cursor() as curr:
        print(curr)
        p.execute_batch(curr, _get_stonk_insert_query(), data)

if __name__ == '__main__':
    run()
    #symbols = ['AMC','GME']
    #fmt = "%Y-%m-%d %H:%M:%S%z"
    #data = get_stonk_data(symbols)
    #print(f"Before: {data}")
    ## convert datetime 
    #for d in data:
    #    d['str_dt'] = get_utc_from_unix_time(d.get('t'))
    #print(f"After: {data}")
