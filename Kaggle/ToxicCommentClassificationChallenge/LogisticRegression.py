
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
import numpy as np
import pandas

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer

#Feature Extraction
#https://stackoverflow.com/questions/34449127/sklearn-tfidf-transformer-how-to-get-tf-idf-values-of-given-words-in-documen
count_vect = CountVectorizer(strip_accents='unicode',
                             analyzer='word',
                             token_pattern=r'\w{1,}',
                             ngram_range = (1,1),max_df = 0.1,
                             stop_words='english')
tfidf_transformer = TfidfTransformer(sublinear_tf=True,
                                     use_idf=False)    
transformer=HashingVectorizer(stop_words='english')
Tfidfvectorizer = TfidfVectorizer(
    sublinear_tf=True,
    strip_accents='unicode',
    analyzer='word',
    token_pattern=r'\w{1,}',
    stop_words='english',
    ngram_range=(1, 1),
    max_features=10000)

#train data
label_cols = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
train = pandas.read_csv('train.csv')#, skiprows=range(1, 140000)) #159571 rows x 8 columns
train_x = train['comment_text']

#Predict data
predict_data = pandas.read_csv('test.csv')#, skiprows=range(1, 140000)) #153164 rows x 2 columns
predict_id = predict_data['id']
predict_x = predict_data['comment_text']

#train_x = transformer.fit_transform(train_x)
#train_x = count_vect.fit_transform(train_x)	
#train_x = tfidf_transformer.fit_transform(train_x)
#predict_x = transformer.fit_transform(predict_x)
#predict_x = count_vect.transform(predict_x)	
#predict_x = tfidf_transformer.transform(predict_x)
Tfidfvectorizer.fit(pandas.concat([train_x, predict_x]))
train_x = Tfidfvectorizer.transform(train_x)
predict_x = Tfidfvectorizer.transform(predict_x)


preds = np.zeros((len(predict_data), len(label_cols)))

scores = []

for i, col in enumerate(label_cols):
    train_y = train[col]
    lr=LogisticRegression(C=1.2)

    cv_score = np.mean(cross_val_score(lr, train_x, train_y, cv=3, scoring='roc_auc'))
    scores.append(cv_score)
    print('CV score for class {} is {}'.format(col, cv_score))

    lr.fit(train_x,train_y)

    preds[:,i] = lr.predict_proba(predict_x)[:, 1]

##col = label_cols[0]
##for i in np.arange(1.4,1.8,0.05):
##    train_y = train[col]
##    lr=LogisticRegression(C=i)
##    cv_score = np.mean(cross_val_score(lr, train_x, train_y, cv=3, scoring='roc_auc'))
##    scores.append(cv_score)
##    print('CV score for c= {} is {}'.format(i, cv_score))


print('Total CV score is {}'.format(np.mean(scores)))

dfid = pandas.DataFrame({'id': predict_id})
submission = pandas.concat([dfid, pandas.DataFrame(preds, columns = label_cols)], axis=1)
submission.to_csv('submission.csv', index=False)
