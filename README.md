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

[YouTube Video: Task0](https://www.youtube.com/watch?v=SYwyHpXaIHg&list=PLgw2ZWQ-nlFxEkIIPrsKcgppuATaLNh0l&index=2)

**Task 1: Create Kinesis Firehose Delivery Stream**

1. Create a Kinesis Firehose delivery stream in AWS console
2. Run a test to send records to Kinesis Firehose, and check the data in S3 bucket
   - Use Fake package to generate data
   - Send the data to the new Kinesis Firehose
   - The Kinesis Firehose Delivery Stream works perfectly.

[YouTube Video: Task1](https://www.youtube.com/watch?v=mFo6bcvfdNY&list=PLgw2ZWQ-nlFxEkIIPrsKcgppuATaLNh0l&index=3)

**Task 2: Add dynamic partitioning with JQ Expression for Kinesis Firehose**
1. Create a Kinesis Firehose delivery stream in AWS console
2. Enable inline parse for json data
3. Add JQ Expression
4. Edit output path based on dynamic partitioning
5. Run a test to send records to Kinesis Firehose, and check the data in S3 bucket
   - The Kinesis Firehose Delivery Stream works perfectly.

[YouTube Video: Task2](https://www.youtube.com/watch?v=DUGLVArexkA&list=PLgw2ZWQ-nlFxEkIIPrsKcgppuATaLNh0l&index=4)

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
6. Good Materials:
- [Dynamic Partitioning in Kinesis Data Firehose.](https://docs.aws.amazon.com/firehose/latest/dev/dynamic-partitioning.html)
- [How does the event coming to Lambda from Firehose look like?](https://docs.aws.amazon.com/lambda/latest/dg/services-kinesisfirehose.html)
- Upload an error_message file, which can help us to understand, when there is an error, how kinesis firehose save the rawData to error path in s3 bucket.

[Youtube video: Task3](https://www.youtube.com/watch?v=y5zlwUjcCLg&list=PLgw2ZWQ-nlFxEkIIPrsKcgppuATaLNh0l&index=5)

**Task 4: Debug of Size Limitation error in Lambda Function for Kinesis Firehose1**
1. Create a supper great data, but afer compress in gzip, it is super small.
- create a function get_size() to check the message size, especially get the real size of dictionary/json data.
2. Check the error of Lambda function and figure out why it hanppens.
- Error 1 in Lambda: [ERROR] [1700244733357] LAMBDA_RUNTIME Failed to post handler success response. Http response code: 413.
- Solution 1:
   - Check the size of data pass to lambda function
   - Check the size of total size of multiple records
   - If the total_size is greater than 5 MB, don't append the record to firehose_records_output
- Error 2 in Kinesis Firehose:[ERROR] One or more record Ids were not returned. Ensure that the Lambda function returns all received record Ids.
- Solution 2:
   - When we return the records from lambda function back to Kinesis Firehose, we need to check send all records back. But the total memory size of the records exceed the size limitation 6 MB, so for the extra records, we still need to append back the firehose_records_output, but change the status from "Ok" to "Drop".
   - Re-ingest the dropped records to the same Kinesis Firehose
   - Check the IAM role to get the permission to PutRecord from Lambda Function to Kinesis Firehose
- Error 3 for IAM role permission: [ERROR] ClientError: An error occurred (AccessDeniedException) when calling the PutRecord operation: User: arn:aws:sts::xxx is not authorized to perform: firehose:PutRecord on resource: arn:aws:firehose:us-west-2:xxx because no identity-based policy allows the firehose:PutRecord action.
- Solution 3:
   - Add PutRecod permission to Kinesis Firehose to Lambda function role
   - The pemission is in PutRecordToFirehosePolicy.json file.
3. Good Materials:
- [Amazon Kinesis Data Firehose Data Transformation](https://docs.aws.amazon.com/firehose/latest/dev/data-transformation.html)
4. Important points for this size issue:
- **6 MB size limitation**: The Lambda synchronous invocation mode has a payload size limit of **6 MB** for both the request and the response. Make sure that your buffering size for sending the request to the function is less than or equal to **6 MB**. Also ensure that the response that your function returns doesn't exceed **6 MB**.
- **Check result for the response**: The status of the data transformation of the record. The possible values are:
   - Ok (the record was transformed successfully)
   - Dropped (the record was dropped intentionally by your processing logic)
   - ProcessingFailed (the record could not be transformed).
   - If a record has a status of Ok or Dropped, Kinesis Data Firehose considers it successfully processed. Otherwise, Kinesis Data Firehose considers it unsuccessfully processed.

**Task 5: Debug of Size Limitation error in Lambda Function for Kinesis Firehose2**
1. Another important edge case
- In task 4, we discuss about the 6MB size limitation for request and response between lambda function and Kinesis Firehose. But we still miss one edge case.
   - What if we only have 1 record, and the compressed record size is less than 6 MB, but the decompressed record size is larger than 6 MB?
   - What will happen from task4 solution? It is no-ending cycle. The lambda function will try to check the size of the output record and reingest this one record to the Kinesis Firehose by trigger the put_record function again and again.
- I guess it will cost a lot of money and we never know there is an non-ending event exist when we send a large set of data.
2. Solution:
- Not only check the toal_size of all records, but also check the size of each record.
- When the size of one record is greater than 6 MB (In the code, I love to check 5 MB, leave some space.)
- Put this one record directly to S3 bucket , following the same order of path in s3.