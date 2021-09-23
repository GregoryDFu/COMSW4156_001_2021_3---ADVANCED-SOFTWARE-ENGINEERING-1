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
        resp = self.validate_move(player, move)
        if resp == "pass":
            self.current_turn = 'p1' if self.current_turn == 'p2' else 'p2'
        return resp

    def validate_move(self, player, move):
        if self.player1 == "" or self.player2 == "":
            return "Two players are required"
        elif str(player) not in self.current_turn:
            return "It is not player {} 's turn".format(player)
        elif self.remaining_moves == 0:
            return "No more remaining moves"
        elif self.game_result != "":
            return "Game result has already been determined"
        else:
            return self.compute_game_state(player, move)

    def compute_game_state(self, player, move):
        col = int(move['column'][-1]) - 1
        self.rowHeights[col] -= 1
        row = self.rowHeights[col]
        if row < 0:
            self.rowHeights[col] = 0
            return "Column is already full"
        color = self.player1 if player == 1 else self.player2
        self.board[row][col] = color
        x = self.checkForWin(color, row, col, 1, 0) + self.checkForWin(color, row, col, -1, 0) - 1
        y = self.checkForWin(color, row, col, 0, 1) + self.checkForWin(color, row, col, 0, -1) - 1
        pos_slope = self.checkForWin(color, row, col, 1, 1) + self.checkForWin(color, row, col, -1, -1) - 1
        neg_slope = self.checkForWin(color, row, col, -1, 1) + self.checkForWin(color, row, col, 1, -1) - 1
        if x >= 4 or y >= 4 or pos_slope >= 4 or neg_slope >= 4:
            self.game_result = color
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
    

'''
Add Helper functions as needed to handle moves and update board and turns
'''


    
