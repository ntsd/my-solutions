
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics import accuracy_score
import numpy as np
import pandas

transformer=HashingVectorizer(stop_words='english')


label_cols = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
train = pandas.read_csv('train.csv')#, skiprows=range(1, 140000)) #159571 rows x 8 columns
train_x = train['comment_text']
train_x = transformer.fit_transform(train_x)

#Train
svm_models = {}
for col in label_cols:
    train_y = train[col]
    svm=LinearSVC()
    svm.fit(train_x,train_y)
    svm_models[col] = svm

#Test Acc
##test = pandas.read_csv('train.csv')#, skiprows=range(10000, 159571))
##test_x = test['comment_text']
##test_x = transformer.fit_transform(test_x)
##for i, col in enumerate(label_cols):
##    test_y = test[col]
##    predict_y = svm_models[col].predict(test_x)
##    accuracy = accuracy_score(test_y, predict_y)
##    print(accuracy)

#Predict data
predict_data = pandas.read_csv('test.csv')#, skiprows=range(1, 140000)) #153164 rows x 2 columns
predict_id = predict_data['id']
predict_x = predict_data['comment_text']
predict_x = transformer.fit_transform(predict_x)

preds = np.zeros((len(predict_data), len(label_cols)))
for i, col in enumerate(label_cols):
    preds[:,i] = svm_models[col].predict(predict_x)
dfid = pandas.DataFrame({'id': predict_id})
submission = pandas.concat([dfid, pandas.DataFrame(preds, columns = label_cols)], axis=1)
submission.to_csv('submission.csv', index=False)

