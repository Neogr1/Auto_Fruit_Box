class PrefixSum2D:
    def __init__(self, grid):
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.grid = [row.copy() for row in grid]
        self.prefix_sum = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        self.prefix_sum[0][0] = self.grid[0][0]
        for r in range(1, self.rows):
            self.prefix_sum[r][0] = self.grid[r][0] + self.prefix_sum[r-1][0]
        for c in range(1, self.cols):
            self.prefix_sum[0][c] = self.grid[0][c] + self.prefix_sum[0][c-1]
        for r in range(1, self.rows):
            for c in range(1, self.cols):
                self.prefix_sum[r][c] = (self.grid[r][c]
                                         + self.prefix_sum[r-1][c]
                                         + self.prefix_sum[r][c-1]
                                         - self.prefix_sum[r-1][c-1])
    
    def update(self, row, col, value):
        delta = value - self.grid[row][col]
        for r in range(row, self.rows):
            for c in range(col, self.cols):
                self.prefix_sum[r][c] += delta
        self.grid[row][col] = value
    
    def query(self, row1, col1, row2, col2):
        res = self.prefix_sum[row2][col2]
        if row1 > 0:
            res -= self.prefix_sum[row1-1][col2]
        if col1 > 0:
            res -= self.prefix_sum[row2][col1-1]
        if row1 > 0 and col1 > 0:
            res += self.prefix_sum[row1-1][col1-1]
        return res
    
    def get_value(self, row, col):
        return self.grid[row][col]

    def get_grid(self):
        return self.grid