from lambda_firehose import lambda_handler
from KinesisFirehose_Lambda import get_data
import base64

data = get_data()
print("data: ", data)
# the kinesis firehose send base64 encode data to Lambda function
data_encoded64 = base64.b64encode(data)
print("data_encoded64: ", data_encoded64)
event = {
  "invocationId": "invoked123",
  "deliveryStreamArn": "aws:lambda:events",
  "region": "us-west-2",
  "records": [
    {
      "data": data_encoded64,
      "recordId": "record1",
      "approximateArrivalTimestamp": 1510772160000,
      "kinesisRecordMetadata": {
        "shardId": "shardId-000000000000",
        "partitionKey": "4d1ad2b9-24f8-4b9d-a088-76e9947c317a",
        "approximateArrivalTimestamp": "2012-04-23T18:25:43.511Z",
        "sequenceNumber": "49546986683135544286507457936321625675700192471156785154",
        "subsequenceNumber": ""
      }
    }
  ]
}

lambda_handler(firehose_records_input = event, context="")