#!/usr/bin/python3

import boto3
import sys
import os 
import time
import json
import io
import yaml

config = {}
config['ALTERNATE_DRIVING_DIRECTION'] = os.environ.get('DR_ALTERNATE_DRIVING_DIRECTION', 'false')
config['AWS_REGION'] = os.environ.get('DR_AWS_APP_REGION', 'us-east-1')
config['CAR_COLOR'] = os.environ.get('DR_CAR_COLOR', 'Red')
config['CAR_NAME'] = os.environ.get('DR_CAR_NAME', 'MyCar')
config['CHANGE_START_POSITION'] = os.environ.get('DR_CHANGE_START_POSITION', 'true')
config['JOB_TYPE'] = 'TRAINING'
config['KINESIS_VIDEO_STREAM_NAME'] = os.environ.get('DR_KINESIS_STREAM_NAME', 'my-kinesis-stream')
config['METRIC_NAME'] = 'TrainingRewardScore'
config['METRIC_NAMESPACE'] = 'AWSDeepRacer'
config['METRICS_S3_BUCKET'] = os.environ.get('DR_LOCAL_S3_BUCKET', 'bucket')
config['METRICS_S3_OBJECT_KEY'] = os.environ.get('DR_LOCAL_S3_MODEL_PREFIX', 'rl-deepracer-sagemaker') + '/metrics/training_metrics.json'
config['MODEL_METADATA_FILE_S3_KEY'] = os.environ.get('DR_LOCAL_S3_CUSTOM_FILES_PREFIX', 'custom_files') + '/model_metadata.json'
config['NUMBER_OF_EPISODES'] = os.environ.get('DR_NUMBER_OF_EPISODES', '0')
config['RACE_TYPE'] = os.environ.get('DR_RACE_TYPE', 'TIME_TRIAL')
config['REWARD_FILE_S3_KEY'] = os.environ.get('DR_LOCAL_S3_CUSTOM_FILES_PREFIX', 'custom_files') + '/reward_function.py'
config['ROBOMAKER_SIMULATION_JOB_ACCOUNT_ID'] = os.environ.get('', 'Dummy')
config['SAGEMAKER_SHARED_S3_BUCKET'] = os.environ.get('DR_LOCAL_S3_BUCKET', 'bucket')
config['SAGEMAKER_SHARED_S3_PREFIX'] = os.environ.get('DR_LOCAL_S3_MODEL_PREFIX', 'rl-deepracer-sagemaker')
config['SIMTRACE_S3_BUCKET'] = os.environ.get('DR_LOCAL_S3_BUCKET', 'bucket')
config['SIMTRACE_S3_PREFIX'] = os.environ.get('DR_LOCAL_S3_MODEL_PREFIX', 'rl-deepracer-sagemaker')
config['TARGET_REWARD_SCORE'] = os.environ.get('DR_TARGET_REWARD_SCORE', 'None')
config['TRAINING_JOB_ARN'] = 'arn:Dummy'
config['WORLD_NAME'] = os.environ.get('DR_WORLD_NAME', 'LGSWide')

s3_endpoint_url = os.environ.get('DR_LOCAL_S3_ENDPOINT_URL', None)
s3_region = config['AWS_REGION']
s3_bucket = config['SAGEMAKER_SHARED_S3_BUCKET']
s3_prefix = config['SAGEMAKER_SHARED_S3_PREFIX']
s3_yaml_name = os.environ.get('DR_LOCAL_S3_PARAMS_FILE', 'training_params.yaml')
yaml_key = os.path.normpath(os.path.join(s3_prefix, s3_yaml_name))

session = boto3.session.Session()
s3_client = session.client('s3', region_name=s3_region, endpoint_url=s3_endpoint_url)

yaml_key = os.path.normpath(os.path.join(s3_prefix, s3_yaml_name))
local_yaml_path = os.path.abspath(os.path.join('/tmp', 'training-params-' + str(round(time.time())) + '.yaml'))

with open(local_yaml_path, 'w') as yaml_file:
    yaml.dump(config, yaml_file, default_flow_style=False, default_style='\'', explicit_start=True)

s3_client.upload_file(Bucket=s3_bucket, Key=yaml_key, Filename=local_yaml_path)
