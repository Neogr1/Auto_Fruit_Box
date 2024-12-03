import random
from scoring.SegmentTree2D import SegmentTree2D
from scoring.PrefixSum2D import PrefixSum2D
from abc import ABC, abstractmethod

class _Policy(ABC):
    ROW_ITER = list(range(10))
    COL_ITER = list(range(17))

    def __init__(self, grid, boxes=[], target_sum=10):
        self.tree = PrefixSum2D(grid)
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.boxes = boxes
        self.target_sum = target_sum

        for box_coords in boxes:
            self._update_tree_in_box(*box_coords)

    def _update_tree_in_box(self, top_row, left_col, bottom_row, right_col):
        for r in range(top_row, bottom_row + 1):
            for c in range(left_col, right_col + 1):
                if self.tree.get_value(r, c) != 0:
                    self.tree.update(r, c, 0)

    def get_score(self):
        return sum(sum(i==0 for i in row) for row in self.tree.get_grid())

    @abstractmethod
    def execute(self):
        '''
        보드에서 제거할 box의 순서를 찾는 알고리즘 구현
        '''
        pass

class GreedySelection_PositionFirst(_Policy):
    def _greedy_select(self):
        for top_row in self.ROW_ITER:
            for left_col in self.COL_ITER:
                for bottom_row in range(top_row, self.rows):
                    for right_col in range(left_col, self.cols):
                        if self.tree.query(top_row, left_col, bottom_row, right_col) == self.target_sum:
                            return (top_row, left_col, bottom_row, right_col)
        return None

    def execute(self):
        while True:
            random.shuffle(self.ROW_ITER)
            random.shuffle(self.COL_ITER)
            box_coords = self._greedy_select()
            if box_coords is None:
                break
            self._update_tree_in_box(*box_coords)
            self.boxes.append(box_coords)
        return self.boxes
    