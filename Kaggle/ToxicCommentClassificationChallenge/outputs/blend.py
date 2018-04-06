import pandas as pd
from sklearn.preprocessing import minmax_scale

lgb = pd.read_csv('lightgbm.csv') # 0.9785
lr_char_n_grams = pd.read_csv('logistic-regression-with-words-and-char-n-grams.csv')  # 0.9788
r_keras = pd.read_csv('why-a-such-low-score-with-r-and-keras.csv') #0.9815
lemmatization_and_pooled_gru = pd.read_csv('lemmatization-and-pooled-gru.csv') #0.982
tfidf_lr= pd.read_csv('tfidf-lr-best.csv')#my own bad
pool_gru_glove = pd.read_csv('pool-gru-glove-best.csv')#my own bad 
pool_gru_fasttext = pd.read_csv('pool-gru-fasttext-best.csv') #my own bad
bi_gru_cnn = pd.read_csv('bi-gru-cnn-best.csv') #my own 0.9840
bi_lstm = pd.read_csv('bi-lstm-best.csv') #my own 0.9847


##best (minmax_scale(bi_lstm[col].values)+\
##      minmax_scale(bi_gru_cnn[col].values)+\
##      minmax_scale(pool_gru_fasttext[col].values)+\
##      minmax_scale(pool_gru_glove[col].values)+\
##      minmax_scale(r_keras[col].values)+\
##      minmax_scale(lr_char_n_grams[col].values)+\
##      minmax_scale(lgb[col].values))/7


blend = bi_lstm.copy()
col = blend.columns

col = col.tolist()
col.remove('id')
# keeping weight of single best model higher than other blends..
blend[col] = (minmax_scale(bi_lstm[col].values)+\
             minmax_scale(bi_gru_cnn[col].values)+\
             minmax_scale(pool_gru_fasttext[col].values)+\
             minmax_scale(pool_gru_glove[col].values)+\
             minmax_scale(r_keras[col].values)+\
             minmax_scale(lr_char_n_grams[col].values)+\
             minmax_scale(lgb[col].values))/7
blend.to_csv("blend-lgb-lr-r_keras-bi_gru_cnn-lstm-gru_pooling.csv", index=False)
