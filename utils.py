from io import BytesIO
import boto3
import PIL
from PIL import Image

s3 = boto3.resource("s3")


def resized_image_url(resized_key, bucket, region):
    return f"https://s3-{region}.amazonaws.com/{bucket}/{resized_key}"


def get_file_from_s3(bucket_name, key):
    try:
        obj = s3.Object(bucket_name=bucket_name, key=key)
        obj_body = obj.get()["Body"].read()
        return obj_body
    except Exception as e:
        print(e)
        raise (e)


def pillow_optimize(obj_stream, size_split):
    try:
        img = Image.open(BytesIO(obj_stream))
        img = img.resize((int(size_split[0]), int(size_split[1])), PIL.Image.ANTIALIAS)
        buffer = BytesIO()
        img.save(buffer, "JPEG", optimize=True, quality=70)
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(e)
        raise (e)


def upload_file_to_s3(buffer, bucket_name, key):
    try:
        obj = s3.Object(bucket_name=bucket_name, key=key)
        obj.put(Body=buffer, ContentType="image/jpeg")
    except Exception as e:
        print(e)
        raise (e)
