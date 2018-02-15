import boto3
import json

s3 = boto3.client('s3')
def lambda_handler(event, context):
  loads = json.loads(event['invokingEvent'])
  bucket_name = loads["configurationItem"]["resourceName"]

  try:
    get_bucket_encryption = s3.get_bucket_encryption(Bucket=bucket_name)

  except Exception:
    put_encryption = s3.put_bucket_encryption(
      Bucket = bucket_name,
      ServerSideEncryptionConfiguration={
        'Rules': [ 
          {
            'ApplyServerSideEncryptionByDefault': { 'SSEAlgorithm': 'AES256' }
          }
        ]
      })
    pass

