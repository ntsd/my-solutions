import pandas as pd
from sklearn.preprocessing import minmax_scale
lr = pd.read_csv('LogisticRegression.csv')
lstm = pd.read_csv('lstm.csv')

blend = lstm.copy()
col = blend.columns

col = col.tolist()
col.remove('id')
# keeping weight of single best model higher than other blends..
blend[col] = 0.5*minmax_scale(lr[col].values)+0.5*minmax_scale(lstm[col].values)
blend.to_csv("blend.csv", index=False)
