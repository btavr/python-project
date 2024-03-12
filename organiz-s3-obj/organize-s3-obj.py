import boto3
from datetime import datetime

today = datetime.today()

todays_date = today.strftime("%d-%m-%Y")

s3_client = boto3.client('s3')

bucket_name = "bruno-org-s3"

list_objects_response = s3_client.list_objects_v2(Bucket=bucket_name)

get_content = list_objects_response.get("Contents")

get_objects_names = []

for item in get_content:
    s3_object_name = item.get("Key")

    get_objects_names.append(s3_object_name)

directory_name = todays_date + "/"

if directory_name not in get_objects_names:
    s3_client.put_object(Bucket=bucket_name, Key=(directory_name))

for item in get_content:
    obj_creation_date = item.get("LastModified").strftime("%d-%m-%Y") + "/"
    object_name = item.get("Key")

    if obj_creation_date == directory_name and "/" not in object_name:
        s3_client.copy_object(Bucket=bucket_name, CopySource=bucket_name+"/"+object_name, Key=directory_name+object_name)
        s3_client.delete_object(Bucket=bucket_name, Key=object_name)
