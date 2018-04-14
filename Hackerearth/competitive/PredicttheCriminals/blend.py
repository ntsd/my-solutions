import pandas as pd
import numpy as np

from sklearn.preprocessing import minmax_scale

bi_lstm = pd.read_csv('bi-lstm.csv') #0.80833
gru = pd.read_csv('gru.csv') # 0.75264


b1 = bi_lstm.copy()

bi_lstm['Criminal'] = minmax_scale(bi_lstm['Criminal'])
gru['Criminal'] = minmax_scale(gru['Criminal'])

b1['Criminal'] = (4 * bi_lstm['Criminal']  + 1 * gru['Criminal'] )/5
    
b1.to_csv('blend_it_all.csv', index = False)

b1['Criminal']=[round(i) for i in b1['Criminal']]

b1.to_csv('blend_it_all_round.csv', index = False)
