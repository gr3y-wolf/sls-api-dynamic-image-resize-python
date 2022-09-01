import os
import json
import logging
from utils import get_file_from_s3
from vips_compressors import choose_compressor

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main(event, context):
    print("Function called...!!!")
    logger().info(json.dumps(event, indent=4))
    BUCKET = os.environ.get("BUCKET", "api-test-xana")
    try:
        img = event["pathParameters"]["image"]
        print(img)
        prefix = "apitestxana/input/images/"
        key = prefix + img
        print("object to grab  ==>> ", key)

        get_img_stream = get_file_from_s3(bucket_name=BUCKET, key=key)
        choose_compressor(get_img_stream)

    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps(e, indent=4)}
        # raise(e)
