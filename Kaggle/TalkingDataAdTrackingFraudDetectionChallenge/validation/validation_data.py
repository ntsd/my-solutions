# Create training and validation data sets that mirror the relationship
#   between the training data and the test data

# Based on my script
#   https://www.kaggle.com/aharless/training-and-validation-data
# which is based on Konrad's script
#   https://www.kaggle.com/konradb/validation-set
# and Alexander Firsov's discussion thread
#   https://www.kaggle.com/c/talkingdata-adtracking-fraud-detection/discussion/51877

import numpy as np
import pandas as pd
import gc

# Data specifications
columns = ['ip', 'app', 'device', 'os', 'channel', 'click_time', 'is_attributed']
dtypes = {
        'ip'            : 'uint32',
        'app'           : 'uint16',
        'device'        : 'uint8',
        'os'            : 'uint16',
        'channel'       : 'uint16',
        'is_attributed' : 'uint8',
        'click_id'      : 'uint32',
        }

nrows=184903891-1
nchunk=150000000
frm=nrows-nchunk
validate_set=9000000

# Training data
print( "Extracting training data...")
training = pd.read_csv( "../input/train.csv",
                        skiprows=range(1,frm),
                        nrows=nchunk,
                        parse_dates=['click_time'],
                        usecols=columns, 
                        dtype=dtypes)
                        
# Validation data
print( "Extracting first chunk of validation data...")
validate_frm = frm - validate_set - 1000000
valid1 = pd.read_csv( "../input/train.csv", 
                      skiprows=range(1,validate_frm), 
                      nrows=validate_set,
                      parse_dates=['click_time'],
                      usecols=columns, 
                      dtype=dtypes)
print( "Extracting second chunk of validation data...")
validate_frm = frm - validate_set - 1000000
valid2 = pd.read_csv( "../input/train.csv", 
                      skiprows=range(1,validate_frm), 
                      nrows=validate_set,
                      parse_dates=['click_time'],
                      usecols=columns, 
                      dtype=dtypes)
valid2 = pd.concat([valid1, valid2])
del valid1
gc.collect()
print( "Extracting third chunk of validation data...")
validate_frm = frm - validate_set  - 1000000
valid3 = pd.read_csv( "../input/train.csv", 
                      skiprows=range(1,validate_frm), 
                      nrows=validate_set,
                      parse_dates=['click_time'],
                      usecols=columns, 
                      dtype=dtypes)
valid3 = pd.concat([valid2,valid3])
del valid2
gc.collect()
validation = valid3
del valid3
gc.collect()

print( "\nTraining data:")
print( training.shape )
print( training.head() )
print( "Saving training data...")
training.to_pickle('training.pkl')
#training.to_csv('training_split_150M.csv')

validation.reset_index(drop=True,inplace=True)
print( "\nValidation data:")
print( validation.shape )
print( validation.head() )
print( "Saving validation data...")
validation.to_pickle('validation.pkl')
#validation.to_csv('validation_split_30M.csv')

test_df = pd.read_csv("../input/test.csv", parse_dates=['click_time'], dtype=dtypes, usecols=['ip','app','device','os', 'channel', 'click_time', 'click_id'])
test_df.to_pickle('test.pkl')

print("\nDone")
