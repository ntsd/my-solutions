from sklearn.svm import LinearSVC 
from sklearn.linear_model import LogisticRegression 
from sklearn.metrics import accuracy_score 
from sklearn.model_selection import cross_val_score 
import numpy as np 
import pandas 
from preprocess import preprocessing 
 
cols=['IFATHER', 'NRCH17_2', 'IRHHSIZ2', 'IIHHSIZ2', 'IRKI17_2', 'IIKI17_2', 'IRHH65_2', 'IIHH65_2', 'PRXRETRY',\
      'PRXYDATA', 'MEDICARE', 'CAIDCHIP', 'CHAMPUS', 'PRVHLTIN', 'GRPHLTIN', 'HLTINNOS', 'HLCNOTYR', 'HLCNOTMO',\
      'HLCLAST', 'HLLOSRSN', 'HLNVCOST', 'HLNVOFFR', 'HLNVREF', 'HLNVNEED', 'HLNVSOR', 'IRMCDCHP', 'IIMCDCHP',\
      'IRMEDICR', 'IIMEDICR', 'IRCHMPUS', 'IICHMPUS', 'IRPRVHLT', 'IIPRVHLT', 'IROTHHLT', 'IIOTHHLT', 'HLCALLFG',\
      'HLCALL99', 'ANYHLTI2', 'IRINSUR4', 'IIINSUR4', 'OTHINS', 'CELLNOTCL', 'CELLWRKNG', 'IRFAMSOC', 'IIFAMSOC',\
      'IRFAMSSI', 'IIFAMSSI', 'IRFSTAMP', 'IIFSTAMP', 'IRFAMPMT', 'IIFAMPMT', 'IRFAMSVC', 'IIFAMSVC', 'IRWELMOS',\
      'IIWELMOS', 'IRPINC3', 'IRFAMIN3', 'IIPINC3', 'IIFAMIN3', 'GOVTPROG', 'POVERTY3', 'TOOLONG', 'TROUBUND',\
      'PDEN10', 'COUTYP2', 'MAIIN102', 'AIIND102', 'ANALWT_C', 'VESTR', 'VEREP'] 

cols=['PRXRETRY', 'IICHMPUS', 'IRMEDICR', 'IIFAMSVC', 'IRKI17_2', 'POVERTY3', 'IFATHER', 'COUTYP2', 'IRHHSIZ2', 'CHAMPUS', 'IRFAMIN3', 'IRINSUR4', 'HLCALL99', 'HLCNOTMO', 'CELLNOTCL', 'IIWELMOS', 'IRWELMOS', 'PRVHLTIN', 'IRPRVHLT', 'CELLWRKNG', 'IIFAMPMT', 'IIFAMSSI', 'PDEN10', 'IRFAMSVC', 'IRPINC3', 'OTHINS', 'HLNVOFFR', 'IIPINC3', 'IRFAMSOC', 'IRFAMPMT', 'IIKI17_2', 'IRFSTAMP', 'IIFAMIN3', 'IRHH65_2', 'HLCALLFG', 'HLCLAST', 'TROUBUND', 'IRFAMSSI', 'GRPHLTIN', 'IIFSTAMP', 'ANYHLTI2', 'IRCHMPUS', 'GOVTPROG', 'IROTHHLT', 'IIFAMSOC', 'IIMEDICR', 'ANALWT_C', 'MEDICARE', 'VESTR', 'IIOTHHLT', 'HLTINNOS', 'PRXYDATA', 'IIHH65_2', 'HLCNOTYR', 'IIMCDCHP', 'AIIND102', 'VEREP', 'NRCH17_2', 'TOOLONG', 'IIPRVHLT', 'CAIDCHIP', 'HLLOSRSN', 'MAIIN102', 'IRMCDCHP']

# to filter -1 rows with preprocess 0.63387 w/0 0.67071  
 
def isnt(*cols): 
    for c in cols: 
        if c==-1: 
            return False 
    return True 
 
 
#train data 
train = pandas.read_csv('criminal_train.csv') 
train = preprocessing(train) #0.68185 with preprocess 
train_x = train[cols] 
train_y = train['Criminal'] 
 
#Predict data 
predict_data = pandas.read_csv('criminal_test.csv') 
predict_data = preprocessing(predict_data) 
predict_id = predict_data['PERID'] 
predict_x = predict_data[cols] 
 
lr=LogisticRegression() 
 
cv_score = np.mean(cross_val_score(lr, train_x, train_y, scoring='accuracy')) 
print('CV score for class is {}'.format(cv_score)) 
 
lr.fit(train_x,train_y) 
 
preds = lr.predict_proba(predict_x) 
 
submission = pandas.DataFrame({'PERID': predict_id})
submission['Criminal'] = preds[:, 1]
submission.to_csv('lr.csv', index=False) 
round_pred = [int(round(i)) for i in preds[:, 1]] #round data to {0,1} 
submission['Criminal'] = round_pred 
submission.to_csv('lr-round.csv', index=False) 
