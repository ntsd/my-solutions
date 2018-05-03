SET datetime=%date:~-10,2%%date:~-7,2%%date:~-4,4%_%time:~0,2%%time:~3,2%%time:~6,2%
call set datetime=%datetime: =%

set BUCKET_NAME=ntsd-bucket-us-central1
set JOB_NAME="talking_data_xgboost_%datetime%"
set JOB_DIR=gs://%BUCKET_NAME%/kaggle/TalkingDataAdTracking/xgboost
set REGION=us-central1
set CONFIG=config.yaml
gcloud ml-engine jobs submit training %JOB_NAME% ^
--job-dir %JOB_DIR% ^
--runtime-version 1.6 ^
--config %CONFIG% ^
--module-name trainer.talkingdata_xgboost ^
--package-path ./trainer ^
--region %REGION% ^
-- ^
--train-file gs://%BUCKET_NAME%/kaggle/TalkingDataAdTracking/input/train.csv ^
--test-file gs://%BUCKET_NAME%/kaggle/TalkingDataAdTracking/input/test.csv