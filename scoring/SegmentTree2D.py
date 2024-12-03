class SegmentTree2D:
    def __init__(self, grid):
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.tree = [[0] * (2 * self.cols) for _ in range(2 * self.rows)]
        
        for r in range(self.rows):
            for c in range(self.cols):
                self.tree[r + self.rows][c + self.cols] = grid[r][c]
        
        for r in range(self.rows, 2 * self.rows):
            for c in range(self.cols - 1, 0, -1):
                self.tree[r][c] = self.tree[r][2 * c] + self.tree[r][2 * c + 1]
        
        for r in range(self.rows - 1, 0, -1):
            for c in range(2 * self.cols):
                self.tree[r][c] = self.tree[2 * r][c] + self.tree[2 * r + 1][c]
    
    def update(self, row, col, value):
        r, c = row + self.rows, col + self.cols
        self.tree[r][c] = value
        
        while c > 1:
            c //= 2
            self.tree[r][c] = self.tree[r][2 * c] + self.tree[r][2 * c + 1]
        
        while r > 1:
            r //= 2
            for c in range(self.cols * 2):
                self.tree[r][c] = self.tree[2 * r][c] + self.tree[2 * r + 1][c]
    
    def query(self, row1, col1, row2, col2):
        res = 0
        r1, r2 = row1 + self.rows, row2 + self.rows
        while r1 <= r2:
            if r1 % 2 == 1:
                c1, c2 = col1 + self.cols, col2 + self.cols
                while c1 <= c2:
                    if c1 % 2 == 1:
                        res += self.tree[r1][c1]
                        c1 += 1
                    if c2 % 2 == 0:
                        res += self.tree[r1][c2]
                        c2 -= 1
                    c1 //= 2
                    c2 //= 2
                r1 += 1
            if r2 % 2 == 0:
                c1, c2 = col1 + self.cols, col2 + self.cols
                while c1 <= c2:
                    if c1 % 2 == 1:
                        res += self.tree[r2][c1]
                        c1 += 1
                    if c2 % 2 == 0:
                        res += self.tree[r2][c2]
                        c2 -= 1
                    c1 //= 2
                    c2 //= 2
                r2 -= 1
            r1 //= 2
            r2 //= 2
        return res
    
    def get_value(self, row, col):
        return self.tree[row + self.rows][col + self.cols]

    def get_grid(self):
        grid = [[0] * self.cols for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                grid[r][c] = self.get_value(r, c)
        return grid