import pandas as pd
import numpy as np

# df = pd.read_csv('/data/sean/trade/pos-20171009.csv')
df = pd.read_csv('/data/sean/revn-50-60/tt-20171009.csv')
df['v'] = df[['action', 'vol']].apply(lambda x: x['vol'] if x['action']=='Open' else -x['vol'], axis = 1)
dfgb = df.groupby(['inst', 'dir'])
dfagg = dfgb.agg('sum')
