import db


class Gameboard():
    def __init__(self):
        self.player1 = ""
        self.player2 = ""
        self.board = [[0 for x in range(7)] for y in range(6)]
        self.game_result = ""
        self.current_turn = 'p1'
        self.remaining_moves = 42
        self.rowHeights = [6 for x in range(7)]

    def handle_move(self, player, move):
        col = int(move['column'][-1]) - 1
        return self.validate_move(player, col)

    def validate_move(self, player, col):
        if self.player1 == "" or self.player2 == "":
            return "Two players are required"
        elif str(player) not in self.current_turn:
            return "It is not player {} 's turn".format(player)
        elif self.remaining_moves == 0:
            return "No more remaining moves"
        elif self.game_result != "":
            return "Game result has already been determined"
        else:
            resp = self.compute_game_state(player, col)
            if resp == "pass":
                self.current_turn = 'p1' if self.current_turn == 'p2' else 'p2'
                move = ((self.current_turn, str(self.board), self.game_result,
                         self.player1, self.player2, self.remaining_moves,
                         str(self.rowHeights)))
                db.add_move(move)
            return resp

    def compute_game_state(self, player, col):
        self.rowHeights[col] -= 1
        row = self.rowHeights[col]
        if row < 0:
            self.rowHeights[col] = 0
            return "Column is already full"
        self.remaining_moves -= 1
        color = self.player1 if player == 1 else self.player2
        self.board[row][col] = color
        x1 = self.checkForWin(color, row, col, 1, 0)
        x2 = self.checkForWin(color, row, col, -1, 0) - 1
        x = x1 + x2
        y1 = self.checkForWin(color, row, col, 0, 1)
        y2 = self.checkForWin(color, row, col, 0, -1) - 1
        y = y1 + y2
        pos_slope1 = self.checkForWin(color, row, col, 1, 1)
        pos_slope2 = self.checkForWin(color, row, col, -1, -1) - 1
        pos_slope = pos_slope1 + pos_slope2
        neg_slope1 = self.checkForWin(color, row, col, -1, 1)
        neg_slope2 = self.checkForWin(color, row, col, 1, -1) - 1
        neg_slope = neg_slope1 + neg_slope2
        if x >= 4 or y >= 4 or pos_slope >= 4 or neg_slope >= 4:
            self.game_result = color
        if self.remaining_moves == 0:
            self.game_result = 'draw'
        return "pass"

    def checkForWin(self, color, row, col, dx, dy):
        max_row = len(self.board)
        max_col = len(self.board[0])
        count = 0
        for i in range(4):
            if row >= 0 and row < max_row and col >= 0 and col < max_col:
                if self.board[row][col] == color:
                    count += 1
                else:
                    return count
            row += dx
            col += dy
        return count
