from faker import Faker
from datetime import datetime
import random
import boto3
import json


def get_data():
    f = Faker()
    table_list = ["table1", "table2", "table3"]
    database_list = ["database1","database2"]
    random_number_list = random.sample(range(1,6), 3)
    print("random_number_list:",random_number_list)
    data = {
        "firstname" : f.unique.first_name(),
        "lastname" : f.unique.last_name(),
        "ssn" : f.unique.ssn(),
        "time" : str(datetime.now()),
        "database" : random.choice(database_list),
        "table" : random.choice(table_list),
        "event_id" : random.choice(random_number_list)
    }
    print(data)
    return data
get_data()

# s3 path: bucket_name/ingest/data/database/table/event_id/year/month/day/hour/file_name


def put_record(payload = None, streamName=None):
    client = boto3.client("firehose")
    client.put_record(
        DeliveryStreamName=streamName,
        Record={"Data":json.dumps(payload)}
    )

# for i in range(20):
#     streamName = "SophieTech-KinesisFirehose-Demo2"
#     data = get_data()
#     put_record(payload = data, streamName=streamName)