import pyautogui as pag

from constant import *

def start_game():
    pag.sleep(DELAY)
    pag.click(930, 680) # click reset
    pag.sleep(DELAY)
    loc = pag.locateOnScreen(PLAY_BUTTON_IMAGE, confidence=0.95)
    if not loc:
        raise Exception("Cannot locate start button.")
    pag.click(loc)
    pag.sleep(DELAY)

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

def play_game(boxes):
    for r1,c1,r2,c2 in boxes:
        _drag_apples(r1,c1,r2,c2)