import random
from SegmentTree2D import SegmentTree2D

ROW_ITER = list(range(10))
COL_ITER = list(range(17))

def _update_tree_box(tree, top_row, left_col, bottom_row, right_col):
    for r in range(top_row, bottom_row + 1):
        for c in range(left_col, right_col + 1):
            if tree.get_value(r, c) != 0:
                tree.update(r, c, 0)

def _find_box_with_sum(tree, rows, cols, target_sum=10):
    for top_row in ROW_ITER:
        for left_col in COL_ITER:
            for bottom_row in range(top_row, rows):
                for right_col in range(left_col, cols):
                    if tree.query(top_row, left_col, bottom_row, right_col) == target_sum:
                        return (top_row, left_col, bottom_row, right_col)
    return None

# find boxes whose sum is 
def find_boxes(grid, boxes=[], target_sum=10, pointer=None):
    tree = SegmentTree2D(grid)
    rows, cols = len(grid), len(grid[0])

    for box_coords in boxes:
        _update_tree_box(tree, *box_coords)

    while True:
        random.shuffle(ROW_ITER)
        random.shuffle(COL_ITER)
        box_coords = _find_box_with_sum(tree, rows, cols, target_sum)
        if box_coords is None:
            break
        _update_tree_box(tree, *box_coords)
        boxes.append(box_coords)
    
    if pointer is not None:
        score = sum(sum(i==0 for i in row) for row in tree.to_grid())
        pointer.append(score)

    return boxes

# kinds of genetic algorithm
def find_best_boxes(grid):
    max_score = 0
    best_boxes = []

    for epoch in range(30):
        print("EPOCH:", epoch)
        for depth in range(5):
            determined_boxes = best_boxes[:depth]
            for _ in range(10):
                pointer = []
                boxes = find_boxes(grid, boxes=determined_boxes, pointer=pointer)
                score = pointer[0]
                if score > max_score:
                    print("Found", score)
                    max_score = score
                    best_boxes = boxes
    
    print("Expected score:", max_score)
    return best_boxes

if __name__ == "__main__":
    grid = [[random.randint(1, 9) for _ in range(17)] for _ in range(10)]
    find_best_boxes(grid)
    for row in grid:
        print(*row)