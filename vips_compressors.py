import pyvips
from io import BytesIO


def choose_compressor(stream):
    try:
        img = pyvips.Image.new_from_source(BytesIO(stream))
        fields = img.get_fields()
        print(fields)
        print(" Good to go for now...")
    except Exception as e:
        print(e)


choose_compressor(BytesIO())
