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

[Youtube video: Task3](https://www.youtube.com/watch?v=y5zlwUjcCLg&list=PLgw2ZWQ-nlFxEkIIPrsKcgppuATaLNh0l&index=5)