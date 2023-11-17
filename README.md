# KinesisFirehoseProject

## Create a Kinesis Firehose pipeline on AWS console

**Task 0: Authentication for boto3**

Purpose: Set the authentication first,then we can use boto3 to connenct to any resources in AWS in the future.

1. Create a new User in IAM role with AdministratorAccess permission
2. Create the credentials and config file under ~/.aws/
3. Test the credentails works
   - create a new s3 bucket
   - upload a file to s3 bucket directly
   - check the s3 bucket name
   - The authentication is set.

**Task 1: Create Kinesis Firehose Delivery Stream**

1. Create a Kinesis Firehose delivery stream in AWS console
2. Run a test to send records to Kinesis Firehose, and check the data in S3 bucket
   - Use Fake package to generate data
   - Send the data to the new Kinesis Firehose
   - The Kinesis Firehose Delivery Stream works perfectly.

**Task 2: Add dynamic partitioning with JQ Expression for Kinesis Firehose**
1. Create a Kinesis Firehose delivery stream in AWS console
2. Enable inline parse for json data
3. Add JQ Expression
4. Edit output path based on dynamic partitioning
5. Run a test to send records to Kinesis Firehose, and check the data in S3 bucket
   - The Kinesis Firehose Delivery Stream works perfectly.

**Task 3: Add dynamic partitioning with Lambda Function for complex data in Kinesis Firehose**
1. The original data is compressed in gzip
2. Create a Lambda function in AWS console
   - decompress the gzip compressed data
   - get the partitioning
   - return the data back with partitioning
3. Create the Kinesis Firehose with dynamic partitioning using the created Lambda function
   - set the s3 destination like: kinesisfirehose-demo/data/database/table/year/month/day/hour/
   - set the s3 error destination like: kinesisfirehose-demo/error/
5. Run a test to send compressed data to Kinesis Firehose, check the data in s3 bucket
6. good materials:
- [Dynamic Partitioning in Kinesis Data Firehose.](https://docs.aws.amazon.com/firehose/latest/dev/dynamic-partitioning.html)
- [How does the event coming to Lambda from Firehose look like?](https://docs.aws.amazon.com/lambda/latest/dg/services-kinesisfirehose.html)
- Upload an error_message file, which can help us to understand, when there is an error, how kinesis firehose save the rawData to error path in s3 bucket.
- [Youtube video]()

**Task 4: Debug of Size Limitation error in Lambda Function for Kinesis Firehose**
1. Create a supper great data, but afer compress in gzip, it is super small.
- create a function get_size() to check the message size, especially get the real size of dictionary/json data.
2. Check the error of Lambda function and figure out why it hanppens.
3. Solve the issue in following steps:
- Check the size of data pass to lambda function
- Check the size of total size of multiple records
- If the total_size is greater than 5 MB, drop the record
- Re-ingest the dropped records to the same Kinesis Firehose
- Check the IAM role to get the permission to PutRecord from Lambda Function to Kinesis Firehose
