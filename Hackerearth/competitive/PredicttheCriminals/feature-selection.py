import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from preprocess import preprocessing 

cols=['IFATHER', 'NRCH17_2', 'IRHHSIZ2', 'IIHHSIZ2', 'IRKI17_2', 'IIKI17_2', 'IRHH65_2', 'IIHH65_2', 'PRXRETRY',\
      'PRXYDATA', 'MEDICARE', 'CAIDCHIP', 'CHAMPUS', 'PRVHLTIN', 'GRPHLTIN', 'HLTINNOS', 'HLCNOTYR', 'HLCNOTMO',\
      'HLCLAST', 'HLLOSRSN', 'HLNVCOST', 'HLNVOFFR', 'HLNVREF', 'HLNVNEED', 'HLNVSOR', 'IRMCDCHP', 'IIMCDCHP',\
      'IRMEDICR', 'IIMEDICR', 'IRCHMPUS', 'IICHMPUS', 'IRPRVHLT', 'IIPRVHLT', 'IROTHHLT', 'IIOTHHLT', 'HLCALLFG',\
      'HLCALL99', 'ANYHLTI2', 'IRINSUR4', 'IIINSUR4', 'OTHINS', 'CELLNOTCL', 'CELLWRKNG', 'IRFAMSOC', 'IIFAMSOC',\
      'IRFAMSSI', 'IIFAMSSI', 'IRFSTAMP', 'IIFSTAMP', 'IRFAMPMT', 'IIFAMPMT', 'IRFAMSVC', 'IIFAMSVC', 'IRWELMOS',\
      'IIWELMOS', 'IRPINC3', 'IRFAMIN3', 'IIPINC3', 'IIFAMIN3', 'GOVTPROG', 'POVERTY3', 'TOOLONG', 'TROUBUND',\
      'PDEN10', 'COUTYP2', 'MAIIN102', 'AIIND102', 'ANALWT_C', 'VESTR', 'VEREP'] 

train = pd.read_csv('criminal_train.csv') 
train = preprocessing(train)
train_x = train[cols]
train_y = train['Criminal']
model = ExtraTreesClassifier()
model.fit(train_x, train_y)
print(list(zip(model.feature_importances_,cols)))
