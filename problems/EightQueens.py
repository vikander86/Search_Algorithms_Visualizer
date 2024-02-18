import copy
from problems import Problem


class EightQueens(Problem):
    def __init__(self):
        super().__init__(initial_state=0, goal_state=8)
        self.chessboard = self.create_board()
        self.index = 0
        self.backtracks = 0
        self.solution = {}

    def create_board(self):
        return [[" " for column in range(8)] for row in range(8)]

    def is_safe(self, row, col):
        for i in range(col):
            if self.chessboard[row][i] == "Q":
                return False

        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if self.chessboard[i][j] == "Q":
                return False

        for i, j in zip(range(row, 8, 1), range(col, -1, -1)):
            if self.chessboard[i][j] == "Q":
                return False
        return True

    def solve(self, col=0):
        if col >= 8:
            return True
        self.index += 1
        self.solution[self.index] = copy.deepcopy(self.chessboard)
        for i in range(8):
            if self.is_safe(i, col):
                self.chessboard[i][col] = "Q"
                if self.solve(col + 1):
                    return True
                self.chessboard[i][col] = " "
                self.backtracks += 1

        return False

    def goal_test(self):
        return self.initial_state == self.goal_state

    def print_board(self):
        for row in self.chessboard:
            print(row)


# test = EightQueens()
# test.solve()
# print(test.solution)
