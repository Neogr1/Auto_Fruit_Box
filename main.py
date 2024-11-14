import os
import pyautogui as pag

from constant import *
from game_play.OCR_Textract import *
from game_play.game_controller import *
import scoring.solver as solver
import scoring.Policy as Policy

def switch_screen():
    pag.shortcut('alt','tab')

def save_board_image():
    board_image = pag.screenshot(region=(BOARD_LEFT, BOARD_TOP, COL*BOX_SIZE, ROW*BOX_SIZE))
    board_image.save(BOARD_IMAGE)
    return board_image

if __name__ == "__main__":
    os.makedirs(TEMP_IMAGE_PATH, exist_ok=True)

    switch_screen()
    start_game()
    print("[INFO] Game is started.")
    
    board_image = save_board_image()
    board_numbers = read_numbers(board_image)
    print("[INFO] Extracted numbers are:")
    for row in board_numbers: print(*row)
    print("[INFO] The numbers of each digit are:")
    print(*[sum(row.count(digit) for row in board_numbers) for digit in range(10)])

    boxes = solver.pseudo_genetic_algorithm(board_numbers, Policy.GreedySelection_PositionFirst, num_epoch=10, max_depth=10, max_iter=10)
    print("[INFO] Selected boxes are:")
    print("   | r1 c1 r2 c2")
    for i,(r1,c1,r2,c2) in enumerate(boxes): print(f"{i:2d} | {r1:2d} {c1:2d} {r2:2d} {c2:2d}")

    play_game(boxes)