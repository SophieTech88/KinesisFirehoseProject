from __future__ import print_function
import base64
import json
import gzip
import sys
import boto3


def get_size(obj, seen=None):
    "Recursively finds size of objects in bytes."
    # print("start function")
    size = sys.getsizeof(obj)
    # print("size start at : ", size)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    # print("obj_id: ", obj_id)
    if obj_id in seen:
        return 0

    # Important mark as seen *before* entering recursion to gracefully handle self re-ferential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        # print("check values, size:",size)
        size += sum([get_size(k, seen) for k in obj.keys()])
        # print("check keys, size: ",size)
    elif hasattr(obj, "__dict__"):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size


def put_record(payload = None, streamName=None):
    client = boto3.client("firehose")
    client.put_record(
        DeliveryStreamName=streamName,
        Record={"Data": payload}
    )


# Signature for all Lambda functions that user must implement
def lambda_handler(firehose_records_input, context):
    print("Received records for processing from DeliveryStream: " + firehose_records_input['deliveryStreamArn']
          + ", Region: " + firehose_records_input['region']
          + ", and InvocationId: " + firehose_records_input['invocationId'])

    # Create return value.
    firehose_records_output = {'records': []}

    # Create result object.
    # Go through records and process them
    total_count_for_received_records = len(firehose_records_input['records'])
    total_size = 0
    total_count = 0
    recordToReingest = []
    recordToReingestCount = 0
    for firehose_record_input in firehose_records_input['records']:
        # Get user payloa
        payload = base64.b64decode(firehose_record_input['data'])
        decompressed = gzip.decompress(payload).decode('utf-8')
        item_json = json.loads(decompressed)
        print("Record that was received")
        # Create output Firehose record and add modified payload and record ID to it.
        firehose_record_output = {}
        partition_keys = {
                          "table": item_json["table"],
                          "year": item_json["time"][0:4],
                          "month": item_json["time"][5:7],
                          "day": item_json["time"][8:10],
                          }
        # Create output Firehose record and add modified payload and record ID to it.
        firehose_record_output = {'recordId': firehose_record_input['recordId'],
                                  'data': base64.b64encode((decompressed+"\n").encode("utf-8")),
                                  'result': 'Ok',
                                  'metadata': { 'partitionKeys': partition_keys }}
        size = round(get_size(firehose_record_output) / 1024 / 1024, 5)
        total_size += size

        # check the total_size of firehose output
        # if it is less than 5 MB, add the firehose_record_output to firehose_records_output
        if total_size <= 5:
            print("The total memory size is less than 5 MB.")
            total_count +=1
        else:
            print("The total memory size is greater than 5 MB.")
            firehose_record_output["data"] = ""
            firehose_record_output["result"] = "Dropped"
            total_size -= size
            recordToReingestCount +=1
            compressed = gzip.compress(decompressed.encode('utf-8'))
            recordToReingest.append(compressed)
        firehose_records_output['records'].append(firehose_record_output)

    if recordToReingestCount > 0:
        print("There are records need to be re-ingest.")
        for record in recordToReingest:
            put_record(payload=record, streamName= "SophieTech-KinesisFirehose-Demo4")
        print("Successfully reingest ",recordToReingestCount , " out of",total_count_for_received_records," to Kinesis Firehose.")

    print("total_size: ", total_size, "MB.")
    print(total_count , "out of ", total_count_for_received_records , " are successfuly sent back to kinesis firehose.")
    # At the end return processed records
    return firehose_records_output
