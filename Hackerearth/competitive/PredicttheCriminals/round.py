import pandas as pd

data = pd.read_csv('bi-lstm.csv')
data["Criminal"] = [int(round(i))for i in data["Criminal"]]
data.to_csv('bi-lstm-round.csv',index=0)
