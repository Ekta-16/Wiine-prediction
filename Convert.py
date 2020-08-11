import pandas as pd

df = pd.read_json(r'winemag_crawled_data.json')
export_csv = df.to_csv(r'New_wine.csv', index=None, header=True)

