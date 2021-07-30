import pandas as pd
import datetime as dt
import yfinance as yf
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_table
import plotly
import plotly.graph_objects as go
import plotly.express as px
from dash.exceptions import PreventUpdate
from flask import Flask, render_template


ticker = [' AAPL','T','BB', 'KO']


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.Label([
    dcc.Dropdown(id="my-dynamic-dropdown", value = ticker, options=[{'label': i,'value': i} for i in ticker])]),
    dcc.Graph(id='graph'),
    dcc.Graph(id='macd'),
    dcc.Graph(id='hist')
    ]
    )
            

@app.callback(
    Output('graph', 'figure'),
    Output('macd', 'figure'),
    Output('hist', 'figure'),
    Input("my-dynamic-dropdown", 'value')
    )


def Stock_Charts(ticker):
    start = dt.datetime.today()-dt.timedelta(1825)
    end = dt.datetime.today()
    stock_data = yf.download(ticker, start, end)
    def MACD(df,a,b,c):
        df = stock_data.copy()
        df['Fast_EMA']=df['Adj Close'].ewm(span = a, min_periods = a).mean()
        df['Slow_EMA']=df['Adj Close'].ewm(span = b, min_periods = b).mean()
        df['MACD'] = df['Fast_EMA']-df['Slow_EMA']
        df['Signal'] = df['MACD'].ewm(span = c, min_periods = c).mean()
        df['Histogram'] = df['MACD'] - df['Signal']
        df.dropna(inplace = True)
        return df
    
    df_1 = MACD(stock_data, 12,26,9)
    Price_df = df_1.reset_index()
    
    df_2 = Price_df.loc[1222:1225][['Date', 'Adj Close', 'MACD', 'Signal', 'Histogram']].set_index('Date')
   
    
    
    def update_options(search_value):
        if not search_value:
            raise PreventUpdate
            return [o for o in ticker if search_value in o["label"]]
    
    
    fig = go.Figure(data=[go.Candlestick(x=Price_df['Date'],
    open=Price_df['Open'],
    high=Price_df['High'],
    low=Price_df['Low'],
    close=Price_df['Close'])])

    fig.update_layout(
    title='Stock Price',
    yaxis_title='Stock',
    shapes = [dict(
    x0='2016-12-09', x1='2016-12-09', y0=0, y1=1, xref='x', yref='paper',
    line_width=2)],
    annotations=[dict(
    x='2016-12-09', y=0.05, xref='x', yref='paper',
    showarrow=False, xanchor='left', text='Candlestick Chart')]
    )
    
    fig1 = px.line(Price_df, x="Date", y=["MACD","Signal"])
    fig1.update_layout(
    title_text="MACD"
    )
    fig1.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    
    )
    
    fig2 = px.histogram(Price_df, x="Histogram")

    fig2.update_layout(
        title_text="MACD Histogram"
    )
    fig2.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    
    return fig, fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)


