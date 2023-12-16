from faker import Faker
from datetime import datetime
import random
import boto3
import json
import gzip
import sys

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

def get_data():
    f = Faker()
    table_list = ["table1", "table2", "table3"]
    # print("random_number_list:",random_number_list)
    data = {
        "firstname" : f.unique.first_name(),
        "lastname" : f.unique.last_name(),
        "ssn" : f.unique.ssn(),
        "time" : str(datetime.now()),
        "table" : random.choice(table_list),
        "example1" : [111] *100000,
        "example2" : [000] *100000,
        "example3" : [2222] *100000,
    }
    # print(data)
    data_string = json.dumps(data)
    # print("data_string:", data_string)

    # Make the data complex
    encoded = data_string.encode('utf-8')
    # print("encoded: ", encoded)
    compressed = gzip.compress(encoded)
    # print("compressed: ", compressed)

    return compressed

# s3 path: bucket_name/ingest/data/table/year/month/day/hour/file_name
def put_record(payload = None, streamName=None):
    client = boto3.client("firehose")
    client.put_record(
        DeliveryStreamName=streamName,
        Record={"Data": payload}
    )

total_size_before = 0
total_size_after = 0
for i in range(5):
    streamName = "SophieTech-KinesisFirehose-Demo4"
    data = get_data()
    total_size_before += get_size(data)
    decompressed = gzip.decompress(data).decode('utf-8')
    total_size_after += get_size(decompressed)
    put_record(payload = data, streamName=streamName)
print("total_size_before send: ", round(total_size_before/1024, 5), "KB.")
print("total_size_after send: ", round(total_size_after/1024/1024, 5), "MB.")