import pandas as pd 
from sklearn.preprocessing import minmax_scale 
lr = pd.read_csv('lr-best.csv') #0.70538
lstm = pd.read_csv('bi-lstm-best.csv') #0.81276
gru = pd.read_csv('gru-best.csv') #0.80402

blend = lstm.copy() 
 
col='Criminal'
##blend[col] = (minmax_scale(lr[col].values)+minmax_scale(lstm[col].values))/2
##blend.to_csv("blend.csv", index=False) 
##blend[col] = [int(round(i)) for i in blend[col]]
##blend.to_csv("blend-round.csv", index=False) #0.75560

lr[col] = [int(round(i)) for i in lr[col]]
lstm[col] = [int(round(i)) for i in lstm[col]]
gru[col] = [int(round(i)) for i in gru[col]]
blend[col] = [1 if lr[col][i]+lstm[col][i]+gru[col][i] > 1 else 0 for i in range(len(lr[col]))]
blend.to_csv("blend-round.csv", index=False) #0.79213
