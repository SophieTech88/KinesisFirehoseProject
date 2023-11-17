
from __future__ import print_function
import base64
import json
import datetime
import gzip

# Signature for all Lambda functions that user must implement
def lambda_handler(firehose_records_input, context):
    print("Received records for processing from DeliveryStream: " + firehose_records_input['deliveryStreamArn']
          + ", Region: " + firehose_records_input['region']
          + ", and InvocationId: " + firehose_records_input['invocationId'])

    # Create return value.
    firehose_records_output = {'records': []}

    # Create result object.
    # Go through records and process them

    for firehose_record_input in firehose_records_input['records']:
        # Get user payloa d
        print("data: ", type(firehose_record_input['data']),firehose_record_input['data'])
        payload = base64.b64decode(firehose_record_input['data'])
        print("payload: ", payload)
        decompressed = gzip.decompress(payload).decode('utf-8')
        print("decompressed: ", decompressed)
        item = decompressed.split("<end>")[0]
        print("item: ", type(item), item)
        item_json = json.loads(item)
        print("item_json: ", type(item_json),item_json)

        print("Record that was received")

        print("\n")
        # Create output Firehose record and add modified payload and record ID to it.
        firehose_record_output = {}
        partition_keys = {"database": item_json["database"],
                          "table": item_json["table"],
                          "event_id": item_json["event_id"],
                          "year": item_json["time"][0:4],
                          "month": item_json["time"][5:7],
                          "day": item_json["time"][8:10],
                          }
        print("partition_keys: ", partition_keys)
        # Create output Firehose record and add modified payload and record ID to it.
        firehose_record_output = {'recordId': firehose_record_input['recordId'],
                                  'data': base64.b64encode((item+"\n").encode("utf-8")),
                                  'result': 'Ok',
                                  'metadata': { 'partitionKeys': partition_keys }}

        # Must set proper record ID
        # Add the record to the list of output records.

        firehose_records_output['records'].append(firehose_record_output)
        print("firehose_records_output: ", firehose_records_output)
    # At the end return processed records
    return firehose_records_output
