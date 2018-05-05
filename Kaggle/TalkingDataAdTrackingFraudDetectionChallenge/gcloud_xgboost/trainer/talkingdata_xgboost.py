# -*- coding: utf-8 -*-

FILENO=1 #To distinguish the output file name.
debug=0  #Whethere or not in debuging mode
gcloud=1

import pandas as pd
import time
import numpy as np
from sklearn.model_selection import train_test_split
import xgboost as xgb
#import lightgbm as lgb
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

def do_next_Click( df,agg_suffix='nextClick', agg_type='float32'):
    
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
        df[new_feature] = (df[all_features].groupby(spec[
            'groupby']).click_time.shift(-1) - df.click_time).dt.seconds.astype(agg_type)
        
        predictors.append(new_feature)
        gc.collect()
    return (df)

def do_prev_Click( df,agg_suffix='prevClick', agg_type='float32'):

    #print(f">> \nExtracting {agg_suffix} time calculation features...\n")
    
    GROUP_BY_NEXT_CLICKS = [
    
    # V1
    # {'groupby': ['ip']},
    # {'groupby': ['ip', 'app']},
    {'groupby': ['ip', 'channel']},
    {'groupby': ['ip', 'os']},
    
    # V3
    #{'groupby': ['ip', 'app', 'device', 'os', 'channel']},
    #{'groupby': ['ip', 'os', 'device']},
    #{'groupby': ['ip', 'os', 'device', 'app']}
    ]

    # Calculate the time to next click for each group
    for spec in GROUP_BY_NEXT_CLICKS:
    
       # Name of new feature
        new_feature = '{}_{}'.format('_'.join(spec['groupby']),agg_suffix)    
    
        # Unique list of features to select
        all_features = spec['groupby'] + ['click_time']

        # Run calculation
        #print(f">> Grouping by {spec['groupby']}, and saving time to {agg_suffix} in: {new_feature}")
        df[new_feature] = (df.click_time - df[all_features].groupby(spec[
                'groupby']).click_time.shift(+1) ).dt.seconds.astype(agg_type)
        
        predictors.append(new_feature)
        gc.collect()
    return (df)    

def do_count( df, group_cols, counted, agg_type='uint8', show_max=False, show_agg=True ):
    agg_name= '{}_by_{}_count'.format(('_'.join(group_cols)),(counted))  
    if show_agg:
        print( "\nCounting ", counted, " by ", group_cols ,  '... and saved in', agg_name )
    gp = df[group_cols+[counted]].groupby(group_cols)[counted].count().reset_index().rename(columns={counted:agg_name})
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

def do_agg( df, group_cols, agg_type='uint8', show_max=False, show_agg=True ):
    agg_name='{}_agg'.format('_'.join(group_cols))  
    if show_agg:
        print( "\nAggregating by ", group_cols ,  '... and saved in', agg_name )
    gp = df[group_cols].groupby(group_cols).size().rename(agg_name).to_frame().reset_index()
    df = df.merge(gp, on=group_cols, how='left')
    del gp
    if show_max:
        print( agg_name + " max value = ", df[agg_name].max() )
    df[agg_name] = df[agg_name].astype(agg_type)
    predictors.append(agg_name)
#     print('predictors',predictors)
    gc.collect()
    return( df )

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

def DO(frm,to,fileno,train_file='gs://ntsd-bucket-us-central1/kaggle/TalkingDataAdTracking/input/train.pkl',
               test_file='gs://ntsd-bucket-us-central1/kaggle/TalkingDataAdTracking/input/test.pkl',
                job_dir='gs://ntsd-bucket-us-central1/kaggle/TalkingDataAdTracking/xgboost', **args):
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

    if gcloud:
        train_df = read_data(train_file, parse_dates=['click_time'], skiprows=range(1,frm), nrows=to-frm, dtype=dtypes, usecols=['ip','app','device','os', 'channel', 'click_time', 'is_attributed'])
    else:
        train_df = pd.read_csv("../input/train.csv", parse_dates=['click_time'], skiprows=range(1,frm), nrows=to-frm, dtype=dtypes, usecols=['ip','app','device','os', 'channel', 'click_time', 'is_attributed'])


    print('loading test data...')
    if gcloud:
        test_df = read_data(test_file, parse_dates=['click_time'], dtype=dtypes, usecols=['ip','app','device','os', 'channel', 'click_time', 'click_id'])
    else:
        if debug:
           test_df = pd.read_csv("../input/test.csv", nrows=1000, parse_dates=['click_time'], dtype=dtypes, usecols=['ip','app','device','os', 'channel', 'click_time', 'click_id'])
        else:
           test_df = pd.read_csv("../input/test.csv", parse_dates=['click_time'], dtype=dtypes, usecols=['ip','app','device','os', 'channel', 'click_time', 'click_id'])

    len_train = len(train_df)
    train_df=train_df.append(test_df)

    del test_df
    gc.collect()

    #add more feature
    train_df['hour'] = pd.to_datetime(train_df.click_time).dt.hour.astype('int8')
    train_df['day'] = pd.to_datetime(train_df.click_time).dt.day.astype('int8')
    train_df['minute'] = pd.to_datetime(train_df.click_time).dt.minute.astype('int8')
#     train_df['second'] = pd.to_datetime(train_df.click_time).dt.second.astype('int8')
    
    if gcloud:
        train_df = do_next_Click( train_df,agg_suffix='nextClick', agg_type='float32'  ); gc.collect()
        train_df = do_prev_Click( train_df,agg_suffix='prevClick', agg_type='float32'  ); gc.collect()  ## Removed temporarily due RAM sortage. 
    train_df = do_countuniq( train_df, ['ip'], 'channel' ); gc.collect()
    train_df = do_countuniq( train_df, ['ip'], 'os' ); gc.collect()
    train_df = do_countuniq( train_df, ['ip'], 'hour' ); gc.collect()
    train_df = do_countuniq( train_df, ['ip'], 'minute' ); gc.collect()
    train_df = do_countuniq( train_df, ['ip'], 'app'); gc.collect()
    train_df = do_countuniq( train_df, ['ip'], 'device'); gc.collect()
    train_df = do_countuniq( train_df, ['app'], 'channel'); gc.collect()
#     train_df = do_countuniq( train_df, ['ip', 'day'], 'hour' ); gc.collect()
#     train_df = do_countuniq( train_df, ['ip', 'app'], 'os'); gc.collect()
    train_df = do_countuniq( train_df, ['ip', 'device'], 'channel' ); gc.collect()
    
    train_df = do_countuniq( train_df, ['ip', 'device', 'os'], 'channel'); gc.collect()
#     train_df = do_countuniq( train_df, ['ip','day','hour'], 'channel' ); gc.collect()
    train_df = do_countuniq( train_df, ['ip','app', 'os'], 'channel' ); gc.collect()
    train_df = do_countuniq( train_df, ['ip', 'device', 'os'], 'app'); gc.collect()
    train_df = do_countuniq( train_df, ['ip','app', 'os', 'device'], 'channel' ); gc.collect()
 

    train_df = do_cumcount( train_df, ['ip'], 'os'); gc.collect()
    train_df = do_cumcount( train_df, ['ip', 'device', 'os'], 'app'); gc.collect()
    
#     train_df = do_count( train_df, ['ip','day','hour'], 'channel' ); gc.collect()
    train_df = do_count( train_df, ['ip','app', 'os'], 'channel' ); gc.collect()
    train_df = do_count( train_df, ['ip','app', 'os', 'device'], 'channel' ); gc.collect()
    
    train_df = do_agg( train_df, ['ip', 'day', 'hour'] ); gc.collect()
    train_df = do_agg( train_df, ['ip', 'app']); gc.collect()
    train_df = do_agg( train_df, ['ip', 'app', 'os']); gc.collect()
#     train_df = do_var( train_df, ['ip', 'day', 'channel'], 'hour'); gc.collect()
    train_df = do_var( train_df, ['ip', 'app', 'os'], 'hour'); gc.collect()
#     train_df = do_var( train_df, ['ip', 'app', 'channel'], 'day'); gc.collect()
#     train_df = do_mean( train_df, ['ip', 'app', 'channel'], 'hour' ); gc.collect()

    del train_df['day']
    gc.collect()

    del train_df['minute']
    gc.collect()

    print('\n\nBefore appending predictors...\n\n',sorted(predictors))
    target = 'is_attributed'
    word= ['app','device','os', 'channel', 'hour']
    for feature in word:
        if feature not in predictors:
            predictors.append(feature)
    
    predictors_sorted= sorted(list(set(predictors)))
    print('\n\nAfter appending predictors...\n\n',predictors_sorted)

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
    start_time = time.time()

    xgb_params ={'eta': 0.3,
                'max_depth': 6,
                'learning_rate': 0.3,
                'n_estimators': 100,
                'silent': False,
                'objective': 'binary:logistic',#'binary:logistic',
                'eval_metric': 'logloss',  # auc
                'nthread':8,
                'gamma': 5.103973694670875e-08,
                'max_delta_step': 20,
                'min_child_weight': 4,
                'subsample': 0.7,
                'colsample_bylevel': 0.1,
                'colsample_bytree': 0.7,
                'reg_alpha': 1e-09,
                'reg_lambda': 1000.0,
                'scale_pos_weight': 499.99999999999994,
                'random_state': 84,
                'tree_method':'hist',
                'grow_policy':'depthwise'
                }
    if gcloud:
        if debug:
            xgb_params['tree_method'] = 'hist'
        else:
            xgb_params['tree_method'] = 'hist'

    xgtrain = xgb.DMatrix(train_df[predictors_sorted].values, label=train_df[target].values)
    xgvalid = xgb.DMatrix(val_df[predictors_sorted].values, label=val_df[target].values)
    del train_df
    del val_df
    gc.collect()
    
    trained_model = xgb.train(xgb_params,xgtrain, 700,[(xgvalid, 'valid')],
                              maximize=True, early_stopping_rounds=50,verbose_eval=10)

    xgbtest=xgb.DMatrix(test_df[predictors_sorted].values)
    print("\nModel Report")
    print("bst1.best_iteration: ", trained_model.best_iteration)

    print('[{}]: model training time'.format(time.time() - start_time))

    # ax = lgb.plot_importance(bst, max_num_features=300)
    # plt.savefig('test%d.png'%(fileno), dpi=600, bbox_inches='tight')
    # plt.show()

    print("Predicting...")
    sub['is_attributed'] = trained_model.predict(xgbtest,ntree_limit=trained_model.best_ntree_limit)

    submit_name = 'xgboost_sub{}_{}_{}.csv'.format(fileno,nchunk,val_size)
    sub.to_csv(submit_name,index=False,float_format='%.9f')

    if gcloud:
        with file_io.FileIO(submit_name, mode='r') as input_f:
            with file_io.FileIO(job_dir + '/' + submit_name, mode='w+') as output_f:
                output_f.write(input_f.read())


    model_name = './model{}_{}_{}.bst'.format(fileno,nchunk,val_size)
    trained_model.save_model(model_name)

    if gcloud:
        # Save the model to the Cloud Storage bucket's jobs directory
        with file_io.FileIO(model_name, mode='r') as input_f:
            with file_io.FileIO(job_dir + '/' + model_name, mode='w+') as output_f:
                output_f.write(input_f.read())
            
    print("done...")


####### Chunk size defining and final run  ############

if __name__ == '__main__':
    nrows=184903891-1
    nchunk=180000000#120000000#150000000
    val_size=9000000#2500000

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
