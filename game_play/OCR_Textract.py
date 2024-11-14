import re
import boto3
from PIL import Image

from constant import *

def _clean_image(image):
    MIN = 14
    MAX = 26
    MARGIN = 10
    pixels = image.load()
    new_width = sum(1 for x in range(image.width) if MIN <= x % BOX_SIZE <= MAX) + MARGIN
    cleaned_image = Image.new("RGB", (new_width, image.height), "white")
    new_x = MARGIN // 2

    for x in range(image.width):
        if not (MIN <= x % BOX_SIZE <= MAX):
            continue
        for y in range(image.height):
            r, g, b = pixels[x, y]
            if (10 <= y % BOX_SIZE <= 30) and (r > 200 and g > 200 and b > 200):
                cleaned_image.putpixel((new_x, y), (0, 0, 0))
            else:
                cleaned_image.putpixel((new_x, y), (255, 255, 255))
        new_x += 1
    
    cleaned_image.save(CLEANED_BOARD_IMAGE)
    return cleaned_image

def _extract_numbers_from_image(image_bytes):
    client = boto3.client('textract')
    response = client.detect_document_text(Document={'Bytes': image_bytes})

    numbers = []
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            text = item["Text"]
            extracted_numbers = re.findall(r'\d+', text)
            int_numbers = list(map(int, extracted_numbers[0]))
            numbers.append(int_numbers)
    
    if len(numbers) != ROW or any(len(row) != COL for row in numbers):
        raise Exception("OCR was not successfully done")
    return numbers

def read_numbers(image):
    cleaned_image = _clean_image(image)
    with open(CLEANED_BOARD_IMAGE, 'rb') as file:
        image_bytes = file.read()
        board_numbers = _extract_numbers_from_image(image_bytes)
    return board_numbers