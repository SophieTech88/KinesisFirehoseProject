import boto3

s3 = boto3.resource('s3')

# Filename - File to upload
# Bucket - Bucket to upload to (the top level directory under AWS S3)
# Key - S3 object name (can contain subdirectories). If not specified then file_name is used
s3.meta.client.upload_file(
    Filename='test.txt',
    Bucket='sophietech-demo',
    Key='data/test.txt'
    )

# print the bucket name
for bucket in s3.buckets.all():
    print(bucket.name)
