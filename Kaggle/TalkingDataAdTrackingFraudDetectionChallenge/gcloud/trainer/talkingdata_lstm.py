# -*- coding: utf-8 -*-
"""
If you find this kernel helpful please upvote. Also any suggestion for improvement will be warmly welcomed.
I made cosmetic changes in the [code](https://www.kaggle.com/aharless/kaggle-runnable-version-of-baris-kanber-s-lightgbm/code). 
Added some new features. Ran for 25mil chunk rows.
Also taken ideas from various public kernels.
"""

FILENO=2 #To distinguish the output file name.
debug=0  #Whethere or not in debuging mode

import pandas as pd
import time
import numpy as np
from sklearn.model_selection import train_test_split
import lightgbm as lgb
import gc
#import matplotlib.pyplot as plt
import os
import argparse
from tensorflow.python.lib.io import file_io # for better file I/O
import sys

###### Feature extraction ######

#### Extracting next click feature 
    ### Taken help from https://www.kaggle.com/nanomathias/feature-engineering-importance-testing
    ###Did some Cosmetic changes 
predictors=[]
def do_next_prev_Click( df,agg_suffix, agg_type='float32'):
    print('Extracting new features...')
    df['hour'] = pd.to_datetime(df.click_time).dt.hour.astype('int8')
    df['day'] = pd.to_datetime(df.click_time).dt.day.astype('int8')
    
    #### New added
    df['minute'] = pd.to_datetime(df.click_time).dt.minute.astype('int8')
    predictors.append('minute')
    df['second'] = pd.to_datetime(df.click_time).dt.second.astype('int8')
    predictors.append('second')
    #print(f">> \nExtracting {agg_suffix} time calculation features...\n")
    
    GROUP_BY_NEXT_CLICKS = [
    
    # V1
    # {'groupby': ['ip']},
    # {'groupby': ['ip', 'app']},
    # {'groupby': ['ip', 'channel']},
    # {'groupby': ['ip', 'os']},
    
    # V3
    {'groupby': ['ip', 'app', 'device', 'os', 'channel']},
    {'groupby': ['ip', 'os', 'device']},
    {'groupby': ['ip', 'os', 'device', 'app']}
    ]

    # Calculate the time to next click for each group
    for spec in GROUP_BY_NEXT_CLICKS:
    
       # Name of new feature
        new_feature = '{}_{}'.format('_'.join(spec['groupby']),agg_suffix)    
    
        # Unique list of features to select
        all_features = spec['groupby'] + ['click_time']

        # Run calculation
        #print(f">> Grouping by {spec['groupby']}, and saving time to {agg_suffix} in: {new_feature}")
        if agg_suffix=="nextClick":
            df[new_feature] = (df[all_features].groupby(spec[
            'groupby']).click_time.shift(-1) - df.click_time).dt.seconds.astype(agg_type)
        elif agg_suffix== "prevClick":
            df[new_feature] = (df.click_time - df[all_features].groupby(spec[
                'groupby']).click_time.shift(+1) ).dt.seconds.astype(agg_type)
        predictors.append(new_feature)
        gc.collect()
#         print('predictors',predictors)
    return (df)

def do_count( df, group_cols, agg_type='uint16', show_max=False, show_agg=True ):
    agg_name='{}count'.format('_'.join(group_cols))  
    if show_agg:
        print( "\nAggregating by ", group_cols ,  '... and saved in', agg_name )
    gp = df[group_cols][group_cols].groupby(group_cols).size().rename(agg_name).to_frame().reset_index()
    df = df.merge(gp, on=group_cols, how='left')
    del gp
    if show_max:
        print( agg_name + " max value = ", df[agg_name].max() )
    df[agg_name] = df[agg_name].astype(agg_type)
    predictors.append(agg_name)
#     print('predictors',predictors)
    gc.collect()
    return( df )

def do_countuniq( df, group_cols, counted, agg_type='uint8', show_max=False, show_agg=True ):
    agg_name= '{}_by_{}_countuniq'.format(('_'.join(group_cols)),(counted))  
    if show_agg:
        print( "\nCounting unqiue ", counted, " by ", group_cols ,  '... and saved in', agg_name )
    gp = df[group_cols+[counted]].groupby(group_cols)[counted].nunique().reset_index().rename(columns={counted:agg_name})
    df = df.merge(gp, on=group_cols, how='left')
    del gp
    if show_max:
        print( agg_name + " max value = ", df[agg_name].max() )
    df[agg_name] = df[agg_name].astype(agg_type)
    predictors.append(agg_name)
#     print('predictors',predictors)
    gc.collect()
    return( df )

def do_cumcount( df, group_cols, counted,agg_type='uint16', show_max=False, show_agg=True ):
    agg_name= '{}_by_{}_cumcount'.format(('_'.join(group_cols)),(counted)) 
    if show_agg:
        print( "\nCumulative count by ", group_cols , '... and saved in', agg_name  )
    gp = df[group_cols+[counted]].groupby(group_cols)[counted].cumcount()
    df[agg_name]=gp.values
    del gp
    if show_max:
        print( agg_name + " max value = ", df[agg_name].max() )
    df[agg_name] = df[agg_name].astype(agg_type)
    predictors.append(agg_name)
#     print('predictors',predictors)
    gc.collect()
    return( df )

def do_mean( df, group_cols, counted, agg_type='float16', show_max=False, show_agg=True ):
    agg_name= '{}_by_{}_mean'.format(('_'.join(group_cols)),(counted))  
    if show_agg:
        print( "\nCalculating mean of ", counted, " by ", group_cols , '... and saved in', agg_name )
    gp = df[group_cols+[counted]].groupby(group_cols)[counted].mean().reset_index().rename(columns={counted:agg_name})
    df = df.merge(gp, on=group_cols, how='left')
    del gp
    if show_max:
        print( agg_name + " max value = ", df[agg_name].max() )
    df[agg_name] = df[agg_name].astype(agg_type)
    predictors.append(agg_name)
#     print('predictors',predictors)
    gc.collect()
    return( df )

def do_var( df, group_cols, counted, agg_type='float16', show_max=False, show_agg=True ):
    agg_name= '{}_by_{}_var'.format(('_'.join(group_cols)),(counted)) 
    if show_agg:
        print( "\nCalculating variance of ", counted, " by ", group_cols , '... and saved in', agg_name )
    gp = df[group_cols+[counted]].groupby(group_cols)[counted].var().reset_index().rename(columns={counted:agg_name})
    df = df.merge(gp, on=group_cols, how='left')
    del gp
    if show_max:
        print( agg_name + " max value = ", df[agg_name].max() )
    df[agg_name] = df[agg_name].astype(agg_type)
    predictors.append(agg_name)
#     print('predictors',predictors)
    gc.collect()
    return( df )

###  A function is written to train the lightGBM model with different given parameters
if debug:
    print('*** debug parameter set: this is a test run for debugging purposes ***')
    
def lgb_modelfit_nocv(params, dtrain, dvalid, predictors, target='target', objective='binary', metrics='auc',
                 feval=None, early_stopping_rounds=30, num_boost_round=3000, verbose_eval=10, categorical_features=None):
    lgb_params = {
        'boosting_type': 'gbdt',
        'objective': objective,
        'metric':metrics,
        'learning_rate': 0.05,
        #'is_unbalance': 'true',  #because training data is unbalance (replaced with scale_pos_weight)
        'num_leaves': 31,  # we should let it be smaller than 2^(max_depth)
        'max_depth': -1,  # -1 means no limit
        'min_child_samples': 20,  # Minimum number of data need in a child(min_data_in_leaf)
        'max_bin': 255,  # Number of bucketed bin for feature values
        'subsample': 0.6,  # Subsample ratio of the training instance.
        'subsample_freq': 0,  # frequence of subsample, <=0 means no enable
        'colsample_bytree': 0.3,  # Subsample ratio of columns when constructing each tree.
        'min_child_weight': 5,  # Minimum sum of instance weight(hessian) needed in a child(leaf)
        'subsample_for_bin': 200000,  # Number of samples for constructing bin
        'min_split_gain': 0,  # lambda_l1, lambda_l2 and min_gain_to_split to regularization
        'reg_alpha': 0,  # L1 regularization term on weights
        'reg_lambda': 0,  # L2 regularization term on weights
        'nthread': 8,
        'verbose': 0,
    }

    lgb_params.update(params)

    print("preparing validation datasets")

    xgtrain = lgb.Dataset(dtrain[predictors].values, label=dtrain[target].values,
                          feature_name=predictors,
                          categorical_feature=categorical_features
                          )
    xgvalid = lgb.Dataset(dvalid[predictors].values, label=dvalid[target].values,
                          feature_name=predictors,
                          categorical_feature=categorical_features
                          )

    evals_results = {}

    bst1 = lgb.train(lgb_params, 
                     xgtrain, 
                     valid_sets=[xgtrain, xgvalid], 
                     valid_names=['train','valid'], 
                     evals_result=evals_results, 
                     num_boost_round=num_boost_round,
                     early_stopping_rounds=early_stopping_rounds,
                     verbose_eval=10, 
                     feval=feval)

    print("\nModel Report")
    print("bst1.best_iteration: ", bst1.best_iteration)
    print(metrics+":", evals_results['valid'][metrics][bst1.best_iteration-1])

    return (bst1,bst1.best_iteration)
    
## Running the full calculation.

#### A function is written here to run the full calculation with defined parameters.

from tensorflow.python.lib.io import file_io
from pandas.compat import StringIO

# read the input data
def read_data(gcs_path, **args):# use this function instead pandas read csv in gcloud ml engine
   print('downloading csv file from', gcs_path)     
   file_stream = file_io.FileIO(gcs_path, mode='r')
   data = pd.read_csv(StringIO(file_stream.read()), **args)
   #print(data.head())
   return data

def DO(frm,to,fileno,train_file='gs://ntsd-bucket/kaggle/TalkingDataAdTracking/input/train.pkl',
               test_file='gs://ntsd-bucket/kaggle/TalkingDataAdTracking/input/test.pkl',
                job_dir='gs://ntsd-bucket/kaggle/TalkingDataAdTracking/lstm', **args):
    dtypes = {
            'ip'            : 'uint32',
            'app'           : 'uint16',
            'device'        : 'uint8',
            'os'            : 'uint8',
            'channel'       : 'uint16',
            'is_attributed' : 'uint8',
            'click_id'      : 'uint32',
            }

    print('loading train data...',frm,to)
    train_df = read_data(train_file, parse_dates=['click_time'], skiprows=range(1,frm), nrows=to-frm, dtype=dtypes, usecols=['ip','app','device','os', 'channel', 'click_time', 'is_attributed'])
    #train_df = read_data(job_dir+"../input/train.csv", parse_dates=['click_time'], skiprows=range(1,frm), nrows=to-frm, dtype=dtypes, usecols=['ip','app','device','os', 'channel', 'click_time', 'is_attributed'])
    # Reading in the pickle file. Pickle works differently with Python 2 vs 3
##    train_f = file_io.FileIO(train_file, mode='r')
##    pandas.read_pickle(train_f)
    
    print('loading test data...')
##    test_f = file_io.FileIO(test_file, mode='r')
##    pandas.read_pickle(test_f)
    test_df = read_data(test_file, parse_dates=['click_time'], dtype=dtypes, usecols=['ip','app','device','os', 'channel', 'click_time', 'click_id'])
    #if debug:
    #    test_df = pd.read_csv("../input/test.csv", nrows=100000, parse_dates=['click_time'], dtype=dtypes, usecols=['ip','app','device','os', 'channel', 'click_time', 'click_id'])
    #else:
    #    test_df = pd.read_csv("../input/test.csv", parse_dates=['click_time'], dtype=dtypes, usecols=['ip','app','device','os', 'channel', 'click_time', 'click_id'])

    
    
    len_train = len(train_df)
    train_df=train_df.append(test_df)
    
    del test_df    
    gc.collect()
    
        
    train_df = do_next_prev_Click( train_df,agg_suffix='nextClick', agg_type='float32'  ); gc.collect()
    train_df = do_next_prev_Click( train_df,agg_suffix='prevClick', agg_type='float32'  ); gc.collect()  ## Removed temporarily due RAM sortage. 
    train_df = do_countuniq( train_df, ['ip'], 'channel' ); gc.collect()
    train_df = do_countuniq( train_df, ['ip', 'device'], 'channel' ); gc.collect()
    train_df = do_countuniq( train_df, ['ip', 'device', 'os'], 'app'); gc.collect()
    train_df = do_countuniq( train_df, ['ip', 'device', 'os'], 'channel'); gc.collect()
    train_df = do_countuniq( train_df, ['ip', 'day'], 'hour' ); gc.collect()
    train_df = do_countuniq( train_df, ['ip'], 'app'); gc.collect()
    train_df = do_countuniq( train_df, ['ip', 'app'], 'os'); gc.collect()
    train_df = do_countuniq( train_df, ['ip'], 'device'); gc.collect()
    train_df = do_countuniq( train_df, ['app'], 'channel'); gc.collect()
    train_df = do_cumcount( train_df, ['ip'], 'os'); gc.collect()
    train_df = do_cumcount( train_df, ['ip', 'device', 'os'], 'app'); gc.collect()
    train_df = do_count( train_df, ['ip', 'day', 'hour'] ); gc.collect()
    train_df = do_count( train_df, ['ip', 'app']); gc.collect()
    train_df = do_count( train_df, ['ip', 'app', 'os']); gc.collect()
    train_df = do_var( train_df, ['ip', 'day', 'channel'], 'hour'); gc.collect()
    train_df = do_var( train_df, ['ip', 'app', 'os'], 'hour'); gc.collect()
    train_df = do_var( train_df, ['ip', 'app', 'channel'], 'day'); gc.collect()
    train_df = do_mean( train_df, ['ip', 'app', 'channel'], 'hour' ); gc.collect()
    
    #print(train_df.head(5))
    gc.collect()
    print('\n\nBefore appending predictors...\n\n',sorted(predictors))
    target = 'is_attributed'
    word= ['app','device','os', 'channel', 'hour', 'day','minute', 'second']
    for feature in word:
        if feature not in predictors:
            predictors.append(feature)
    categorical = ['app', 'device', 'os', 'channel', 'hour', 'day','minute', 'second']
    print('\n\nAfter appending predictors...\n\n',sorted(predictors))

    test_df = train_df[len_train:]
    val_df = train_df[(len_train-val_size):len_train]
    train_df = train_df[:(len_train-val_size)]

    print("train size: ", len(train_df))
    print("valid size: ", len(val_df))
    print("test size : ", len(test_df))

    sub = pd.DataFrame()
    sub['click_id'] = test_df['click_id'].astype('int')

    gc.collect()

    print("Training...")
    #start_time = time.time()

    params = {
        'learning_rate': 0.20,
        #'is_unbalance': 'true', # replaced with scale_pos_weight argument
        'num_leaves': 7,  # 2^max_depth - 1
        'max_depth': 3,  # -1 means no limit
        'min_child_samples': 100,  # Minimum number of data need in a child(min_data_in_leaf)
        'max_bin': 100,  # Number of bucketed bin for feature values
        'subsample': 0.7,  # Subsample ratio of the training instance.
        'subsample_freq': 1,  # frequence of subsample, <=0 means no enable
        'colsample_bytree': 0.9,  # Subsample ratio of columns when constructing each tree.
        'min_child_weight': 0,  # Minimum sum of instance weight(hessian) needed in a child(leaf)
        'scale_pos_weight':200 # because training data is extremely unbalanced 
    }
    (bst,best_iteration) = lgb_modelfit_nocv(params, 
                            train_df, 
                            val_df, 
                            predictors, 
                            target, 
                            objective='binary', 
                            metrics='auc',
                            early_stopping_rounds=30, 
                            verbose_eval=True, 
                            num_boost_round=1000, 
                            categorical_features=categorical)

    #print('[{}]: model training time'.format(time.time() - start_time))
    del train_df
    del val_df
    gc.collect()

    print("Predicting...")
    sub['is_attributed'] = bst.predict(test_df[predictors],num_iteration=best_iteration)
           
    submit_name = 'sub_it%d.csv'%(fileno)
    sub.to_csv(submit_name,index=False,float_format='%.9f')
    with file_io.FileIO(submit_name, mode='r') as input_f:
        with file_io.FileIO(job_dir + '/' + submit_name, mode='w+') as output_f:
            output_f.write(input_f.read())


    model_name = 'model%d.txt'%(fileno)
    bst.save_model(model_name)
    
    # Save the model to the Cloud Storage bucket's jobs directory
    with file_io.FileIO(model_name, mode='r') as input_f:
        with file_io.FileIO(job_dir + '/' + model_name, mode='w+') as output_f:
            output_f.write(input_f.read())
            
    print("done...")
    
    
####### Chunk size defining and final run  ############

if __name__ == '__main__':
    nrows=184903891-1
    nchunk=184900000#80000000
    val_size=14900000#2500000

    frm=nrows-nchunk

    if debug:
        val_size = 500
        frm = 0
        nchunk = 5000

    to=frm+nchunk

    parser = argparse.ArgumentParser()
    parser.add_argument(
      '--train-file',
      help='Cloud Storage bucket or local path to training data')
    parser.add_argument(
      '--test-file',
      help='Cloud Storage bucket or local path to test data')
    parser.add_argument(
      '--job-dir',
      help='Cloud storage bucket to export the model and store temp files')
    args = parser.parse_args()
    arguments = args.__dict__
    
    DO(frm,to,FILENO,**arguments)
