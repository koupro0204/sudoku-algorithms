import copy
from generator import SudokuGenerator
import random

class SudokuPuzzleGenerator(SudokuGenerator):
    def __init__(self):
        super().__init__()

    def remove_numbers(self, level):
        """Remove numbers from the grid based on difficulty level."""
        if level == "easy":
            numbers_to_remove = 20
        elif level == "medium":
            numbers_to_remove = 40
        elif level == "hard":
            numbers_to_remove = 63
        elif level == "expert":
            numbers_to_remove = 70
        else:  # expert
            numbers_to_remove = 73

        attempts = numbers_to_remove
        while attempts > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            while self.grid[row][col] == 0:
                row = random.randint(0, 8)
                col = random.randint(0, 8)
            
            backup = self.grid[row][col]
            self.grid[row][col] = 0

            # Create a copy of the grid for solving
            grid_copy = copy.deepcopy(self.grid)
            solver = SudokuSolver(grid_copy)
            solver.solve()

            if not solver.is_unique_solution():
                self.grid[row][col] = backup
                attempts -= 1
            print(f"Attempt: {numbers_to_remove - attempts}/{numbers_to_remove}", end='\r')


    def generate_puzzle(self, difficulty_level):
        """Generate a Sudoku puzzle with the specified difficulty level."""
        self.generate()
        self.remove_numbers(difficulty_level)
        return self.grid


class SudokuSolver:
    def __init__(self, grid):
        self.grid = grid
        self.solutions = 0

    def solve(self):
        """Solve the Sudoku puzzle using a backtracking algorithm."""
        find = self.find_empty_location()
        if not find:
            self.solutions += 1
            return True
        else:
            row, col = find

        for num in range(1, 10):
            if self.is_safe(row, col, num):
                self.grid[row][col] = num
                self.solve()
                self.grid[row][col] = 0

        return False

    def find_empty_location(self):
        """Find an empty location in the grid."""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

    def is_safe(self, row, col, num):
        """Check if it's safe to place num at the specified location."""
        return not self.used_in_row(row, num) and not self.used_in_col(col, num) and not self.used_in_box(row - row % 3, col - col % 3, num)

    def used_in_row(self, row, num):
        """Check if num is used in the specified row."""
        return any(self.grid[row][i] == num for i in range(9))

    def used_in_col(self, col, num):
        """Check if num is used in the specified column."""
        return any(self.grid[i][col] == num for i in range(9))

    def used_in_box(self, box_start_row, box_start_col, num):
        """Check if num is used in the specified 3x3 box."""
        return any(self.grid[i][j] == num for i in range(box_start_row, box_start_row + 3) for j in range(box_start_col, box_start_col + 3))

    def is_unique_solution(self):
        """Check if the Sudoku puzzle has a unique solution."""
        return self.solutions == 1

# Example usage
puzzle_generator = SudokuPuzzleGenerator()
dificulty = ["easy", "medium", "hard", "expert", "master"]
selected_difficulty = dificulty[4]
print(selected_difficulty)

puzzle = puzzle_generator.generate_puzzle(selected_difficulty)  # Generate a medium difficulty puzzle
print(puzzle)

