import pandas as pd

df = pd.read_csv('dj_beta_7.csv')
df2 = df.sort_values('Beta')

df.to_csv('dj_beta_orderd.csv')