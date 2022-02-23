#%%
from Historic_Crypto import HistoricalData
from Historic_Crypto import Cryptocurrencies
from Historic_Crypto import LiveCryptoData
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller


#%%
df = HistoricalData('BTC-USD',86400,'2020-01-01-00-00').retrieve_data()

#%%
result = adfuller(df['close'])
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
	print('\t%s: %.3f' % (key, value))

#%%  
df = df.drop(columns=['volume'])

#%% 
df['weekdays'] = df.index.dayofweek.map({0: "Monday", 1:"Tuesday", 2:"Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"})
df['day'] = df.index.day

#%%
df['avg_price'] = df.loc[:, ['low', 'high', 'open', 'close']].mean(axis=1)


#%%
df.groupby(['year', 'month'])[['avg_price']].min()

#%%

df = df.set_index(['year', 'month', 'day', 'weekdays'])

#%% 
df.groupby([df.index.year, df.index.month])[['avg_price']].idxmin().reset_index(drop=True)
#%%
df_min = df.groupby([df.index.year, df.index.month])[['avg_price']].idxmin()

#%%
df_min.assign(day = df_min['avg_price'].dt.day,
              weekdays = df_min['avg_price'])

#%%
# data = Cryptocurrencies(coin_search = 'XLM', extended_output=False).find_crypto_pairs()

# 
# fig = go.Figure(data=[go.Candlestick(x=df.index,
#                 open=df['open'],
#                 high=df['high'],
#                 low=df['low'],
#                 close=df['close'])])
# fig.show()


# %%

# Create figure with secondary y-axis
# fig = make_subplots(specs=[[{"secondary_y": True}]])

# # include candlestick with rangeselector
# fig.add_trace(go.Candlestick(x=df.index,
#                 open=df['open'], high=df['high'],
#                 low=df['low'], close=df['close']),
#                secondary_y=True)

# # include a go.Bar trace for volumes
# fig.add_trace(go.Bar(x=df.index, y=df['volume']),
#                secondary_y=False)

# fig.layout.yaxis2.showgrid=False
# fig.show()



# %%
