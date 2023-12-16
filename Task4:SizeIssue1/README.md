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
