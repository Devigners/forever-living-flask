import pandas as pd

df = pd.read_csv('static\\web-assets\\data\\blogs\\blogs_small.csv')
print(df)

df.to_json('static\\web-assets\\data\\blogs\\blogs_small.json', orient='index')
