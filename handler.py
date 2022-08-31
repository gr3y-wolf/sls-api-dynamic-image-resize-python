import datetime
import json
import os
import logging
from utils import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def resize_image(bucket_name, key, size):
    try:
        size_split = size.split("x")
        obj_body = get_file_from_s3(bucket_name, key)
        print(obj_body)
        optimized = pillow_optimize(obj_body, size_split)
        resized_key = key.replace("input/images", "test")
        logger.info(resized_key)
        upload_file_to_s3(optimized, bucket_name, resized_key)
        return resized_image_url(resized_key, bucket_name, os.environ["AWS_REGION"])
    except Exception as error:
        logger.info(error)
        raise (error)


def call(event, context):
    try:
        key = event["pathParameters"]["image"]
        size = event["pathParameters"]["size"]
        prefix = "apitestxana/input/images/"
        key = prefix + key
        print("object to grab  ==>> ", key)

        result_url = resize_image(os.environ["BUCKET"], key, size)
        print("result url ==>>>", result_url)

        response = {"statusCode": 200, "body": json.dumps({"result": result_url})}
        return response
    except Exception as e:
        logger.error("error occured in lambda execution")
        print(e)
        # raise(e)
        return {
            "statusCode": "500",
            "body": e,
        }
