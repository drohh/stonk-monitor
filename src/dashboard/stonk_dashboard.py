import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque
import plotly.express as px
from datetime import datetime
from utils.db import WarehouseConnection
from utils.psql_config import get_warehouse_creds


#X=[]
#Y=[]
# deques for live graphs, ref: https://www.geeksforgeeks.org/plot-live-graphs-using-python-dash-and-plotly/
#X = deque(maxlen = 20)
#Y = deque(maxlen = 20)

app = dash.Dash(__name__)

get_stonk_companies_query = "SELECT * FROM stonk.companies;"
get_latest_date_query = "SELECT * FROM stonk.quotes ORDER BY datetime DESC LIMIT 1;"
# pass latest_date into the quotes query below when using psycopg2
get_latest_quotes_query = "SELECT * FROM stonk.quotes WHERE datetime > (%s) - interval '15 minutes';"
# get_latest_quotes_query = "SELECT * FROM stonk.quotes WHERE datetime > now() - interval '1 minute';"

data_company = []
data_price = []
data_datetime = []
fmt = "%Y-%m-%d %H:%M:%S%z"

with WarehouseConnection(get_warehouse_creds()).managed_cursor() as cur:
    cur.execute(get_latest_date_query)
    latest_date = cur.fetchone()[9]
    cur.execute(get_latest_quotes_query, (latest_date,))
    quotes = cur.fetchall()
    cur.execute(get_stonk_companies_query)
    companies = cur.fetchall()

    company_map = {row[0]:row[1] for row in companies}

    for row in quotes:
        data_company.append(company_map.get(row[1]))
        data_price.append(row[2])
        data_datetime.append(row[9]) 
        #data_datetime.append(datetime.strptime(row[9], fmt)) 

fig = px.line(dict(stonk=data_company, price=data_price, datetime=data_datetime), x='datetime', y='price', color='stonk')

app.layout = html.Div(
	[
		dcc.Graph(
            id = 'da-graph',
            figure = fig
        )
	]
)

if __name__ == '__main__':
	app.run_server()

