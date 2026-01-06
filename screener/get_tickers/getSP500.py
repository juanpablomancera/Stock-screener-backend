import pandas as pd

def getSP500():
    payload=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    first_table = payload[0]
    df = first_table
    df.head()
    symbols = df['Symbol'].values.tolist()
    return symbols






