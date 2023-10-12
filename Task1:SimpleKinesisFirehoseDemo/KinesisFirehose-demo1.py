from faker import Faker
from datetime import datetime
import random
import boto3
import json
import time

## download Faker library first
## pip install faker

def get_data():
    f = Faker()
    table_list = ["table1", "table2", "table3"]
    data = {
        "firstname" : f.unique.first_name(),
        "lastname" : f.unique.last_name(),
        "ssn" : f.unique.ssn(),
        "time" : str(datetime.now()),
        "table" : random.choice(table_list)
    }
    return data

def put_record(payload = None, streamName=None):
    client = boto3.client("firehose")
    client.put_record(
        DeliveryStreamName=streamName,
        Record={"Data":json.dumps(payload)}
    )

for i in range(20):
    streamName = "SophieTech-KinesisFirehose-Demo"
    data = get_data()
    print(data)
    put_record(payload = data, streamName=streamName)