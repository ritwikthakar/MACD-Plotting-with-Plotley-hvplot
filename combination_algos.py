#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import yfinance as yf
import talib
import datetime as dt
import matplotlib.pyplot as plt
import mplfinance as mpf
import streamlit as st
ticker = st.sidebar.text_input('Enter Ticker', 'SPY')
t = st.sidebar.selectbox('Select Number of Days', ( 400, 150, 60, 15, 1))
i = st.sidebar.selectbox('Select Time Granularity', ( '1d', '4h', '1h', '15m', '1m'))


# In[2]:


# def trading_algo(t, ticker = 'ticker', i = 'i'):
#     start = dt.datetime.today()-dt.timedelta(t)
#     end = dt.datetime.today()
#     df = yf.download(ticker, start, end, interval = i)
#     slowk, slowd = talib.STOCH(df['High'], df['Low'], df['Adj Close'], fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
#     df['slowk'] = slowk
#     df['slowd'] = slowd
#     df['RSI'] = talib.RSI(df['Adj Close'], timeperiod=14)
#     df['ROCR'] = talib.ROCR(df['Adj Close'], timeperiod=10)
#     macd, macdsignal, macdhist = talib.MACD(df['Adj Close'], fastperiod=12, slowperiod=26, signalperiod=9)
#     df['macd'] = macd
#     df['macdsignal'] = macdsignal
#     df['macdhist'] = macdhist
#     df['50 MA'], df['200 MA'] = talib.MA(df['Adj Close'], timeperiod=50, matype=0), talib.MA(df['Adj Close'], timeperiod=200, matype=0)
#     df['9 MA'], df['21 MA'] = talib.MA(df['Adj Close'], timeperiod=9, matype=0), talib.MA(df['Adj Close'], timeperiod=21, matype=0)
#     df['PSAR'] = real = talib.SAR(df['High'], df['Low'], acceleration=0.02, maximum=0.2)
#     df['upperband'], df['middleband'], df['lowerband'] = talib.BBANDS(df['Adj Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
#     df['ATR'] = talib.ATR(df['High'], df['Low'], df['Adj Close'], timeperiod=14)
#     df['ADX'] = talib.ADX(df['High'], df['Low'], df['Adj Close'], timeperiod=14)
#     df.dropna(inplace=True)
#     colors = ['g' if v >= 0 else 'r' for v in df["macdhist"]]
#     macd_plot = mpf.make_addplot(df["macd"], panel=1, color='blue', title="MACD")
#     macd_hist_plot = mpf.make_addplot(df["macdhist"], type='bar', panel=1, color=colors) # color='dimgray'
#     macd_signal_plot = mpf.make_addplot(df["macdsignal"], panel=1, color='red')
#     rsi_plot = mpf.make_addplot(df["RSI"], panel=2, color='blue', title="RSI")
#     slowk_plot = mpf.make_addplot(df["slowk"], panel=3, color='blue', title="Stochastic Oscillators")
#     slowd_plot = mpf.make_addplot(df["slowd"], panel=3, color='red')
#     psar = mpf.make_addplot(df["PSAR"], type = 'scatter', color='black', markersize = 0.5, title = 'Parabolic Stop & Reverse (PSAR)')
#     fast_ma_l = mpf.make_addplot(df["9 MA"], color='blue', title = 'Technical Indicators')
#     slow_ma_l = mpf.make_addplot(df["21 MA"], color='yellow')
#     fast_ma = mpf.make_addplot(df["50 MA"], color='green')
#     slow_ma = mpf.make_addplot(df["200 MA"], color='red')
#     atr_plot = mpf.make_addplot(df["ATR"], panel=4, color='orange', title="ATR")
#     adx_plot = mpf.make_addplot(df["ADX"], panel=5, color='purple', title="ADX")
#     plots_so = [macd_plot, macd_signal_plot, macd_hist_plot, rsi_plot,slowk_plot,slowd_plot,psar, fast_ma, slow_ma, fast_ma_l, slow_ma_l,atr_plot,adx_plot]
#     fig, axes = mpf.plot(df,type='candle',addplot=plots_so,figscale=1.5,figratio=(32,30), figsize=(24, 24), title=f"\n{ticker}",
#                      style='yahoo',volume=True,volume_panel=6,returnfig=True)
    


# # In[3]:


# fig = trading_algo(400, ticker, '1d')
# plt.savefig('fig.png', bbox_inches='tight')

# # In[ ]:


# st.image(fig)


# In[ ]:


def get_data(t, ticker = 'ticker', i = 'i'):
    start = dt.datetime.today()-dt.timedelta(t)
    end = dt.datetime.today()
    df = yf.download(ticker, start, end, interval = i)
    return df




df = get_data(t, ticker, i)
df





def indicators(df):   
    slowk, slowd = talib.STOCH(df['High'], df['Low'], df['Adj Close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    df['slowk'] = slowk
    df['slowd'] = slowd
    df['RSI'] = talib.RSI(df['Adj Close'], timeperiod=14)
    df['ROCR'] = talib.ROCR(df['Adj Close'], timeperiod=10)
    macd, macdsignal, macdhist = talib.MACD(df['Adj Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['macd'] = macd
    df['macdsignal'] = macdsignal
    df['macdhist'] = macdhist
    df['50 MA'], df['200 MA'] = talib.MA(df['Adj Close'], timeperiod=50, matype=0), talib.MA(df['Adj Close'], timeperiod=200, matype=0)
    df['9 MA'], df['21 MA'] = talib.MA(df['Adj Close'], timeperiod=9, matype=0), talib.MA(df['Adj Close'], timeperiod=21, matype=0)
    df['PSAR'] = real = talib.SAR(df['High'], df['Low'], acceleration=0.02, maximum=0.2)
    df['upperband'], df['middleband'], df['lowerband'] = talib.BBANDS(df['Adj Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    df['ATR'] = talib.ATR(df['High'], df['Low'], df['Adj Close'], timeperiod=14)
    df['ADX'] = talib.ADX(df['High'], df['Low'], df['Adj Close'], timeperiod=14)
    df.dropna(inplace=True)
    return df





df = indicators(df)
df.tail(5)




# macd panel
colors = ['g' if v >= 0 else 'r' for v in df["macdhist"]]
macd_plot = mpf.make_addplot(df["macd"], panel=1, color='blue', title="MACD")
macd_hist_plot = mpf.make_addplot(df["macdhist"], type='bar', panel=1, color=colors) # color='dimgray'
macd_signal_plot = mpf.make_addplot(df["macdsignal"], panel=1, color='red')
rsi_plot = mpf.make_addplot(df["RSI"], panel=2, color='blue', title="RSI")
slowk_plot = mpf.make_addplot(df["slowk"], panel=3, color='blue', title="Stochastic Oscillators")
slowd_plot = mpf.make_addplot(df["slowd"], panel=3, color='red')
psar = mpf.make_addplot(df["PSAR"], type = 'scatter', color='black', markersize = 0.5, title = 'Parabolic Stop & Reverse (PSAR)')
fast_ma_l = mpf.make_addplot(df["9 MA"], color='blue', title = 'Technical Indicators')
slow_ma_l = mpf.make_addplot(df["21 MA"], color='yellow')
fast_ma = mpf.make_addplot(df["50 MA"], color='green')
slow_ma = mpf.make_addplot(df["200 MA"], color='red')
atr_plot = mpf.make_addplot(df["ATR"], panel=4, color='orange', title="ATR")
adx_plot = mpf.make_addplot(df["ADX"], panel=5, color='purple', title="ADX")
# ub_plot = mpf.make_addplot(df["upperband"], color='black')
# lb_plot = mpf.make_addplot(df["lowerband"], color='black')
# mb_plot = mpf.make_addplot(df["middleband"], color='royalblue')


# plot
plots_so = [macd_plot, macd_signal_plot, macd_hist_plot, rsi_plot,slowk_plot,slowd_plot,psar, fast_ma, slow_ma, fast_ma_l, slow_ma_l, atr_plot, adx_plot]
fig, axes = mpf.plot(df,type='candle',addplot=plots_so,figscale=1.5,figratio=(32,30),title=f"\n{ticker}",
                     style='yahoo',volume=True,volume_panel=6,returnfig=True)


st.pyplot(fig)

# In[ ]:





# In[ ]:




