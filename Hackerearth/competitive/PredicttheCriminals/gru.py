<<<<<<< Updated upstream
import numpy as np
np.random.seed(42)
import pandas as pd

import os
from keras.layers import Dense,Input,LSTM,Bidirectional,Activation,Conv1D,GRU
from keras.callbacks import Callback
from keras.layers import Dropout,Embedding,GlobalMaxPooling1D, MaxPooling1D, Add, Flatten
from keras.preprocessing import text, sequence
from keras.layers import GlobalAveragePooling1D, GlobalMaxPooling1D, concatenate, SpatialDropout1D
from keras import initializers, regularizers, constraints, optimizers, layers, callbacks
from keras.callbacks import EarlyStopping,ModelCheckpoint
from keras.models import Model
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import keras.backend as K

from preprocess import preprocessing 

def matthews_correlation(y_true, y_pred):
    y_pred_pos = K.round(K.clip(y_pred, 0, 1))
    y_pred_neg = 1 - y_pred_pos

    y_pos = K.round(K.clip(y_true, 0, 1))
    y_neg = 1 - y_pos

    tp = K.sum(y_pos * y_pred_pos)
    tn = K.sum(y_neg * y_pred_neg)

    fp = K.sum(y_neg * y_pred_pos)
    fn = K.sum(y_pos * y_pred_neg)

    numerator = (tp * tn - fp * fn)
    denominator = K.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))

    return numerator / (denominator + K.epsilon())

cols=['IFATHER', 'NRCH17_2', 'IRHHSIZ2', 'IIHHSIZ2', 'IRKI17_2', 'IIKI17_2', 'IRHH65_2', 'IIHH65_2', 'PRXRETRY',\
                 'PRXYDATA', 'MEDICARE', 'CAIDCHIP', 'CHAMPUS', 'PRVHLTIN', 'GRPHLTIN', 'HLTINNOS', 'HLCNOTYR', 'HLCNOTMO',\
                 'HLCLAST', 'HLLOSRSN', 'HLNVCOST', 'HLNVOFFR', 'HLNVREF', 'HLNVNEED', 'HLNVSOR', 'IRMCDCHP', 'IIMCDCHP',\
                 'IRMEDICR', 'IIMEDICR', 'IRCHMPUS', 'IICHMPUS', 'IRPRVHLT', 'IIPRVHLT', 'IROTHHLT', 'IIOTHHLT', 'HLCALLFG',\
                 'HLCALL99', 'ANYHLTI2', 'IRINSUR4', 'IIINSUR4', 'OTHINS', 'CELLNOTCL', 'CELLWRKNG', 'IRFAMSOC', 'IIFAMSOC',\
                 'IRFAMSSI', 'IIFAMSSI', 'IRFSTAMP', 'IIFSTAMP', 'IRFAMPMT', 'IIFAMPMT', 'IRFAMSVC', 'IIFAMSVC', 'IRWELMOS',\
                 'IIWELMOS', 'IRPINC3', 'IRFAMIN3', 'IIPINC3', 'IIFAMIN3', 'GOVTPROG', 'POVERTY3', 'TOOLONG', 'TROUBUND',\
                 'PDEN10', 'COUTYP2', 'MAIIN102', 'AIIND102', 'ANALWT_C', 'VESTR', 'VEREP']

cols=['PRXRETRY', 'IICHMPUS', 'IRMEDICR', 'IIFAMSVC', 'IRKI17_2', 'POVERTY3', 'IFATHER', 'COUTYP2', 'IRHHSIZ2', 'CHAMPUS', 'IRFAMIN3', 'IRINSUR4', 'HLCALL99', 'HLCNOTMO', 'CELLNOTCL', 'IIWELMOS', 'IRWELMOS', 'PRVHLTIN', 'IRPRVHLT', 'CELLWRKNG', 'IIFAMPMT', 'IIFAMSSI', 'PDEN10', 'IRFAMSVC', 'IRPINC3', 'OTHINS', 'HLNVOFFR', 'IIPINC3', 'IRFAMSOC', 'IRFAMPMT', 'IIKI17_2', 'IRFSTAMP', 'IIFAMIN3', 'IRHH65_2', 'HLCALLFG', 'HLCLAST', 'TROUBUND', 'IRFAMSSI', 'GRPHLTIN', 'IIFSTAMP', 'ANYHLTI2', 'IRCHMPUS', 'GOVTPROG', 'IROTHHLT', 'IIFAMSOC', 'IIMEDICR', 'ANALWT_C', 'MEDICARE', 'VESTR', 'IIOTHHLT', 'HLTINNOS', 'PRXYDATA', 'IIHH65_2', 'HLCNOTYR', 'IIMCDCHP', 'AIIND102', 'VEREP', 'NRCH17_2', 'TOOLONG', 'IIPRVHLT', 'CAIDCHIP', 'HLLOSRSN', 'MAIIN102', 'IRMCDCHP']

train = pd.read_csv('criminal_train.csv')
test = pd.read_csv('criminal_test.csv')

# to filter -1 rows

def isnt(*cols):
    for c in cols:
        if c==-1:
            return False
    return True

def isnt2(*cols):
    for c in cols:
        if c==-1:
            return True
    return False

##train = train[train[cols].apply(lambda x: isnt(*x), axis=1)]
##test_missing = test[test[cols].apply(lambda x: isnt2(*x), axis=1)]
##test = test[test[cols].apply(lambda x: isnt(*x), axis=1)]

train = preprocessing(train)
test = preprocessing(test)

X_train = train[cols]

y_train = train["Criminal"]

X_test = test[cols]

max_features=200000 # max value of data
maxlen=len(cols) #70 # len of input
embed_size=300

def get_model():
    inp = Input(shape=(maxlen, ))
    x = Embedding(max_features, embed_size ,trainable = False)(inp)
    x = SpatialDropout1D(0.2)(x)
    x = Bidirectional(GRU(128, return_sequences=True))(x) #80
    avg_pool = GlobalAveragePooling1D()(x)
    max_pool = GlobalMaxPooling1D()(x)
    conc = concatenate([avg_pool, max_pool])
    outp = Dense(1, activation="sigmoid")(conc)
    
    model = Model(inputs=inp, outputs=outp)
    model.compile(loss='binary_crossentropy',
                  optimizer=Adam(lr=1e-3),
                  metrics=['accuracy'])

    return model

model = get_model()


batch_size = 128
epochs = 8
X_tra, X_val, y_tra, y_val = train_test_split(X_train, y_train, train_size=0.9)

filepath="best.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
early = EarlyStopping(monitor="val_acc", mode="max", patience=5)
callbacks_list = [checkpoint, early]

model.fit(X_tra, y_tra, batch_size=batch_size, epochs=epochs, validation_data=(X_val, y_val),callbacks = callbacks_list,verbose=1)
#Loading model weights
model.load_weights(filepath)
y_pred = model.predict(X_test,batch_size=1024,verbose=1)

submission = pd.DataFrame()
submission['PERID'] = test['PERID'] #pd.concat([test['PERID'], test_missing['PERID']])
submission['Criminal'] = y_pred #np.append(y_pred, np.array([0 for _ in range(len(test_missing))]))
submission.to_csv('gru.csv', index=False)
=======
import numpy as np
np.random.seed(42)
import pandas as pd

import os
from keras.layers import Dense,Input,LSTM,Bidirectional,Activation,Conv1D,GRU
from keras.callbacks import Callback
from keras.layers import Dropout,Embedding,GlobalMaxPooling1D, MaxPooling1D, Add, Flatten
from keras.preprocessing import text, sequence
from keras.layers import GlobalAveragePooling1D, GlobalMaxPooling1D, concatenate, SpatialDropout1D
from keras import initializers, regularizers, constraints, optimizers, layers, callbacks
from keras.callbacks import EarlyStopping,ModelCheckpoint
from keras.models import Model
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import keras.backend as K

def matthews_correlation(y_true, y_pred):
    y_pred_pos = K.round(K.clip(y_pred, 0, 1))
    y_pred_neg = 1 - y_pred_pos

    y_pos = K.round(K.clip(y_true, 0, 1))
    y_neg = 1 - y_pos

    tp = K.sum(y_pos * y_pred_pos)
    tn = K.sum(y_neg * y_pred_neg)

    fp = K.sum(y_neg * y_pred_pos)
    fn = K.sum(y_pos * y_pred_neg)

    numerator = (tp * tn - fp * fn)
    denominator = K.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))

    return numerator / (denominator + K.epsilon())

cols=['IFATHER', 'NRCH17_2', 'IRHHSIZ2', 'IIHHSIZ2', 'IRKI17_2', 'IIKI17_2', 'IRHH65_2', 'IIHH65_2', 'PRXRETRY',\
                 'PRXYDATA', 'MEDICARE', 'CAIDCHIP', 'CHAMPUS', 'PRVHLTIN', 'GRPHLTIN', 'HLTINNOS', 'HLCNOTYR', 'HLCNOTMO',\
                 'HLCLAST', 'HLLOSRSN', 'HLNVCOST', 'HLNVOFFR', 'HLNVREF', 'HLNVNEED', 'HLNVSOR', 'IRMCDCHP', 'IIMCDCHP',\
                 'IRMEDICR', 'IIMEDICR', 'IRCHMPUS', 'IICHMPUS', 'IRPRVHLT', 'IIPRVHLT', 'IROTHHLT', 'IIOTHHLT', 'HLCALLFG',\
                 'HLCALL99', 'ANYHLTI2', 'IRINSUR4', 'IIINSUR4', 'OTHINS', 'CELLNOTCL', 'CELLWRKNG', 'IRFAMSOC', 'IIFAMSOC',\
                 'IRFAMSSI', 'IIFAMSSI', 'IRFSTAMP', 'IIFSTAMP', 'IRFAMPMT', 'IIFAMPMT', 'IRFAMSVC', 'IIFAMSVC', 'IRWELMOS',\
                 'IIWELMOS', 'IRPINC3', 'IRFAMIN3', 'IIPINC3', 'IIFAMIN3', 'GOVTPROG', 'POVERTY3', 'TOOLONG', 'TROUBUND',\
                 'PDEN10', 'COUTYP2', 'MAIIN102', 'AIIND102', 'ANALWT_C', 'VESTR', 'VEREP']

train = pd.read_csv('criminal_train.csv')
test = pd.read_csv('criminal_test.csv')

# to filter -1 rows

def isnt(*cols):
    for c in cols:
        if c==-1:
            return False
    return True

def isnt2(*cols):
    for c in cols:
        if c==-1:
            return True
    return False

train = train[train[cols].apply(lambda x: isnt(*x), axis=1)]
test_missing = test[test[cols].apply(lambda x: isnt2(*x), axis=1)]
test = test[test[cols].apply(lambda x: isnt(*x), axis=1)]

X_train = train[cols]

y_train = train["Criminal"]

X_test = test[cols]

max_features=200000 # max value of data
maxlen=70 # len of input
embed_size=300

def get_model():
    inp = Input(shape=(maxlen, ))
    x = Embedding(max_features, embed_size)(inp)
    x = SpatialDropout1D(0.2)(x)
    x = Bidirectional(GRU(80, return_sequences=True))(x)
    avg_pool = GlobalAveragePooling1D()(x)
    max_pool = GlobalMaxPooling1D()(x)
    conc = concatenate([avg_pool, max_pool])
    outp = Dense(1, activation="sigmoid")(conc)
    
    model = Model(inputs=inp, outputs=outp)
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    return model

model = get_model()


batch_size = 128
epochs = 8
X_tra, X_val, y_tra, y_val = train_test_split(X_train, y_train, train_size=0.9)

filepath="best.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
early = EarlyStopping(monitor="val_acc", mode="max", patience=5)
callbacks_list = [checkpoint, early]

model.fit(X_tra, y_tra, batch_size=batch_size, epochs=epochs, validation_data=(X_val, y_val),callbacks = callbacks_list,verbose=1)
#Loading model weights
model.load_weights(filepath)
y_pred = model.predict(X_test,batch_size=1024,verbose=1)

submission = pd.DataFrame()
submission['PERID'] = pd.concat([test['PERID'], test_missing['PERID']])
submission['Criminal'] = np.append(y_pred, np.array([0 for _ in range(len(test_missing))]))
submission.to_csv('gru.csv', index=False)
>>>>>>> Stashed changes
