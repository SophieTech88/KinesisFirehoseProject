# KinesisFirehoseProject

## Create a Kinesis Firehose pipeline on AWS console

**Task 1: Authentication for boto3**
Purpose: Set the authentication first,then we can use boto3 to connenct to any resources in AWS in the future. 

1. Create a new User in IAM role with AdministratorAccess permission
2. Create the credentials and config file under ~/.aws/
3. Test the credentails works
    - create a new s3 bucket
    - upload a file to s3 bucket directly
    - check the s3 bucket name
The authentication is set.

**Task 2: Create Kinesis Firehose Delivery Stream**

1. Create a Kinesis Firehose delivery stream in AWS console
2. Create `KinesisFirehose.py` file
   - Create KinesisFirehose class
   - set the stream name in `def __init__` function
   - create `def describe()` to check the basic information of the Kinesis Firehose delivery stream
   - create `def put_record()` to put record directly to that Kinesis Firehose delivery stream
3. Run a test to send records to Kinesis Firehose, and check the data in S3 bucket

**Task 3: Add dynamic partitioning with Lambda Function for Kinesis Firehose**
1. The original data is compressed in gzip
2. Create a Lambda function in AWS console
   - decompress the gzip compressed data
   - get the partitioning
   - return the data back with partitioning
3. Create the Kinesis Firehose with dynamic partitioning using the created Lambda function
   - set the s3 destination like: kinesisfirehose-demo/data/database/table/year/month/day/hour/
   - set the s3 error destination like: kinesisfirehose-demo/error/
5. Run a test to send compressed data to Kinesis Firehose, check the data in s3 bucket

