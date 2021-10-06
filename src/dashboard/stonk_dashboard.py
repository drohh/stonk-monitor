import dash
import pandas as pd
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


def layout():
    get_stonk_companies_query = "SELECT * FROM stonk.companies;"
    get_latest_date_query = "SELECT datetime FROM stonk.quotes ORDER BY datetime DESC LIMIT 1;"
    # pass latest_date into the quotes query below when using psycopg2
    get_latest_quotes_query = "SELECT company_id,current_price,datetime FROM stonk.quotes WHERE datetime > (%s) - interval '15 minutes';"
    # get_latest_quotes_query = "SELECT * FROM stonk.quotes WHERE datetime > now() - interval '1 minute';"

    data_company = []
    data_price = []
    data_datetime = []
    fmt = "%Y-%m-%d %H:%M:%S%z"

    with WarehouseConnection(get_warehouse_creds()).managed_cursor() as cur:
        cur.execute(get_latest_date_query)
        latest_date = cur.fetchone()[0]
        cur.execute(get_latest_quotes_query, (latest_date,))
        quotes = cur.fetchall()
        cur.execute(get_stonk_companies_query)
        companies = cur.fetchall()

        company_map = {row[0]:row[1] for row in companies}

        for row in quotes:
            data_company.append(company_map.get(row[0]))
            data_price.append(row[1])
            data_datetime.append(row[2]) 

    df = pd.DataFrame(dict(stonk=data_company, price=data_price, datetime=data_datetime))
    divs = []
    for s, tdf in df.groupby("stonk"):
        fig = px.line(tdf, x='datetime', y='price', markers=True)
        divs.append(
            html.Div([
                html.H1(f'{s}'),
                dcc.Graph(
                    id = f'graph-{s.replace(" ","").lower()}',
                    figure = fig
                )
            ])

        )
    #fig = px.line(dict(stonk=data_company, price=data_price, datetime=data_datetime), x='datetime', y='price', color='stonk', markers=True)

#    return  html.Div(
#                [
#                    html.H1('Hello Dash'),
#                    dcc.Graph(
#                        id = 'da-graph',
#                        figure = fig
#                    )
#                ]
#            )
    return html.Div(children=divs)

#app.layout = html.Div(
#	[
#		dcc.Graph(
#            id = 'da-graph',
#            figure = fig
#        )
#	]
#)

app = dash.Dash(__name__)
app.layout = layout

if __name__ == '__main__':
	app.run_server(host='0.0.0.0')

