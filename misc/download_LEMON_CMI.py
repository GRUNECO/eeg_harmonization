#!pip install -U boto3
import boto3

BUCKET = 'fcp-indi'
#BASE_PREFIX = 'data/Projects/INDI/MPI-LEMON/' #Compressed_tar/MRI_MPILMBB_LEMON/MRI/'
BASE_PREFIX = 'data/Projects/EEG_Eyetracking_CMI_data/' #Compressed_tar/MRI_MPILMBB_LEMON/MRI/'

def list_files(bucket: str = BUCKET, prefix: str = BASE_PREFIX):

  s3_client = boto3.client('s3', aws_access_key_id='', aws_secret_access_key='')
  s3_client._request_signer.sign = (lambda *args, **kwargs: None)
  res = s3_client.list_objects_v2(Bucket=BUCKET, MaxKeys=1000, Prefix=BASE_PREFIX)

  keys = list()
  while res["IsTruncated"]:
    res = s3_client.list_objects_v2(Bucket=BUCKET, MaxKeys=1000, Prefix=BASE_PREFIX, ContinuationToken=res["NextContinuationToken"])
    keys += [item['Key'] for item in res['Contents']]
  return keys