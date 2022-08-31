import datetime
import json
import os
from utils import *


def resize_image(bucket_name, key, size):
    try:
        size_split = size.split("x")
        obj_body = get_file_from_s3(bucket_name, key)
        optimized = pillow_optimize(obj_body, size_split)
        resized_key = "{size}_{key}".format(size=size, key=key)
        upload_file_to_s3(optimized, bucket_name, resized_key)
        return resized_image_url(resized_key, bucket_name, os.environ["AWS_REGION"])
    except Exception as error:
        print(error)
        raise (error)


def call(event, context):
    key = event["pathParameters"]["image"]
    size = event["pathParameters"]["size"]

    result_url = resize_image(os.environ["BUCKET"], key, size)

    response = {
        "statusCode": 301,
        "body": {"result": result_url},
        "headers": {"location": result_url},
    }

    return response
