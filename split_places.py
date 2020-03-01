import pandas as pd

df = pd.read_csv('./data/places.csv')
df.index.name = 'id'

for i in range(0, 3300000, 100000):
    dfslice = df[i:i+100000]
    dfslice.to_csv(f'./data/places_{i+100000}.csv')