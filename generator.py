import numpy as np
import random

class SudokuGenerator:
    def __init__(self):
        self.grid = np.zeros((9, 9), dtype=int)

    def fill_grid(self):
        """Fill the grid using a backtracking algorithm."""
        find = self.find_empty_location()
        if not find:
            return True
        else:
            row, col = find

        for num in range(1, 10):
            if self.is_safe(row, col, num):
                self.grid[row][col] = num
                if self.fill_grid():
                    return True
                self.grid[row][col] = 0
        return False

    def find_empty_location(self):
        """Find an empty location in the grid."""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

    def used_in_row(self, row, num):
        """Check if num is used in the specified row."""
        return any(self.grid[row][i] == num for i in range(9))

    def used_in_col(self, col, num):
        """Check if num is used in the specified column."""
        return any(self.grid[i][col] == num for i in range(9))

    def used_in_box(self, box_start_row, box_start_col, num):
        """Check if num is used in the specified 3x3 box."""
        return any(self.grid[i][j] == num for i in range(box_start_row, box_start_row + 3) for j in range(box_start_col, box_start_col + 3))

    def is_safe(self, row, col, num):
        """Check if it's safe to place num at the specified location."""
        return not self.used_in_row(row, num) and not self.used_in_col(col, num) and not self.used_in_box(row - row % 3, col - col % 3, num)

    def shuffle_grid(self):
        """Shuffle the numbers in the grid to add randomness."""
        # Shuffle rows within each 3-row sector
        for i in range(0, 9, 3):
            rows = list(range(i, i+3))
            random.shuffle(rows)
            self.grid[i:i+3] = self.grid[rows]

        # Shuffle columns within each 3-column sector
        for i in range(0, 9, 3):
            cols = list(range(i, i+3))
            random.shuffle(cols)
            self.grid[:, i:i+3] = self.grid[:, cols]

    def is_valid_grid(self):
        """Check if a given Sudoku grid is valid."""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    num = self.grid[i][j]
                    self.grid[i][j] = 0  # Temporarily empty the cell for validation
                    if not self.is_safe(i, j, num):
                        return False
                    self.grid[i][j] = num  # Restore the original number
        return True

    def generate(self):
        """Generate a random and valid Sudoku grid."""
        self.fill_grid()
        self.shuffle_grid()
        return self.grid

# Example usage
generator = SudokuGenerator()
generated_grid = generator.generate()
is_valid = generator.is_valid_grid()

print(generated_grid)
print(is_valid)
