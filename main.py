import os
import re
import boto3
from PIL import Image
import pyautogui as pag

from find_boxes import find_boxes, find_best_boxes

BOX_SIZE = 41
COL = 17
ROW = 10
BOARD_LEFT = 918
BOARD_TOP = 210
DELAY = 0.5
DRAG_TIME = 0.3
DRAG_STEP = 20
STEP_DELAY = 0.1
PLAY_BUTTON_IMAGE = "img/play_button.png"
BOARD_IMAGE = "img/tmp/game_board.png"
CLEANED_BOARD_IMAGE = "img/tmp/cleaned_game_board.png"


def _save_board_image():
    board_image = pag.screenshot(region=(BOARD_LEFT, BOARD_TOP, COL*BOX_SIZE, ROW*BOX_SIZE))
    board_image.save(BOARD_IMAGE)
    return board_image

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

def _drag_apples(r1, c1, r2, c2):
    x_origin = BOARD_LEFT + c1 * BOX_SIZE
    y_origin = BOARD_TOP + r1 * BOX_SIZE
    x_target = BOARD_LEFT + (c2+1) * BOX_SIZE
    y_target = BOARD_TOP + (r2+1) * BOX_SIZE

    pag.mouseDown(x_origin, y_origin)
    pag.moveTo(x_target, y_target, duration=DRAG_TIME)
    pag.sleep(0.1)
    pag.moveTo(x_target+2, y_target+2)
    pag.sleep(0.1)
    pag.mouseUp()


def switch_screen():
    pag.shortcut('alt','tab')

def start_game():
    pag.click(930, 680) # click reset
    pag.sleep(DELAY)
    loc = pag.locateOnScreen(PLAY_BUTTON_IMAGE, confidence=0.95)
    if not loc:
        raise Exception("Cannot locate start button.")
    pag.click(loc)

def read_numbers_on_board():
    board_image = _save_board_image()
    cleaned_image = _clean_image(board_image)
    with open("img/tmp/cleaned_game_board.png", 'rb') as file:
        image_bytes = file.read()
        board_numbers = _extract_numbers_from_image(image_bytes)
    return board_numbers

def play_game(steps):
    for r1,c1,r2,c2 in steps:
        _drag_apples(r1,c1,r2,c2)
        pag.sleep(STEP_DELAY)

if __name__ == "__main__":
    os.makedirs('img/tmp', exist_ok=True)
    switch_screen()
    
    pag.sleep(DELAY)
    start_game()
    print("[INFO] Game is started.")

    pag.sleep(DELAY)
    board_numbers = read_numbers_on_board()
    print("[INFO] Extracted numbers are:")
    print("[INFO] Numbers of each digit are:", *[sum(row.count(i) for row in board_numbers) for i in range(10)])
    for row in board_numbers: print(*row)

    # boxes = find_boxes(board_numbers)
    boxes = find_best_boxes(board_numbers)
    print(boxes)
    play_game(boxes)

