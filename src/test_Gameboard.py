import unittest
from Gameboard import Gameboard
import db


class Test_TestGameboard(unittest.TestCase):
    def setUp(self):
        self.game_board = Gameboard()
        self.game_board.player1 = 'red'
        self.game_board.player2 = 'yellow'
        db.init_db()

    def test_valid_move(self):
        # Checks that gameboard is properly updated on a valid move
        col = 1
        self.game_board.validate_move(1, col)
        self.assertEqual(self.game_board.board[5][1], 'red')

    def test_valid_move_db(self):
        # Checks that validate move properly adds to db
        col = 1
        self.game_board.validate_move(1, col)
        res = db.getMove()
        self.assertEqual(res[0], 'p2')
        self.assertTrue('red' in res[1])
        self.assertEqual(res[2], '')
        self.assertEqual(res[3], 'red')
        self.assertEqual(res[4], 'yellow')
        self.assertEqual(res[5], 41)
        self.assertEqual(res[6], '[6, 5, 6, 6, 6, 6, 6]')

    def test_winning_move_horizontal(self):
        # Checks if there is a winning move in horizontal direction
        for i in range(3):
            self.game_board.validate_move(1, i)
            self.game_board.validate_move(2, 6)
        self.game_board.validate_move(1, 3)
        self.assertEqual(self.game_board.game_result, 'red')

    def test_winning_move_vertical(self):
        # Checks if there is a winning move in vertical direction
        for i in range(1, 4):
            self.game_board.validate_move(1, 1)
            self.game_board.validate_move(2, 6)
        self.game_board.validate_move(1, 1)
        self.assertEqual(self.game_board.game_result, 'red')

    def test_winning_move_pos_slope(self):
        # Checks if there is a winning move in horizontal direction
        self.game_board.board = [[0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 'red', 'yellow', 0, 0, 0],
                                 [0, 'red', 'yellow', 'yellow', 0, 0, 0],
                                 ['red', 'yellow', 'yellow', 'yellow', 0, 0, 0]
                                 ]
        self.game_board.rowHeights = [5, 4, 3, 3, 6, 6, 6]
        self.game_board.validate_move(1, 3)
        self.assertEqual(self.game_board.game_result, 'red')

    def test_winning_move_neg_slope(self):
        # Checks if there is a winning move in horizontal direction
        self.game_board.board = [[0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 'yellow', 'red', 0, 0],
                                 [0, 0, 0, 'yellow', 'yellow', 'red', 0],
                                 [0, 0, 0, 'yellow', 'yellow', 'yellow', 'red']
                                 ]
        self.game_board.rowHeights = [6, 6, 6, 3, 3, 4, 5]
        self.game_board.validate_move(1, 3)
        self.assertEqual(self.game_board.game_result, 'red')

    def test_invalid_turn(self):
        # Checks if game discards out of order turn and with error
        self.game_board.validate_move(1, 1)
        self.assertEqual(self.game_board.validate_move(1, 1),
                         'It is not player 1 \'s turn')

    def test_winner_already_declared(self):
        # Checks if game discards move after winner declared with error
        for i in range(1, 4):
            self.game_board.validate_move(1, 1)
            self.game_board.validate_move(2, 6)
        self.game_board.validate_move(1, 1)
        self.assertEqual(self.game_board.validate_move(2, 4),
                         'Game result has already been determined')

    def test_draw(self):
        # Checks if the game result works properly on a draw
        self.game_board.board = [[0, 'red', 'yellow', 'red', 'yellow',
                                 'yellow', 'red'],
                                 ['red', 'red', 'yellow', 'red', 'yellow',
                                  'red', 'red'],
                                 ['yellow', 'yellow', 'red', 'yellow', 'red',
                                  'yellow', 'yellow'],
                                 ['yellow', 'red', 'red', 'yellow', 'red',
                                  'red', 'yellow'],
                                 ['yellow', 'red', 'yellow', 'red', 'yellow',
                                  'red', 'yellow'],
                                 ['red', 'yellow', 'red', 'yellow', 'red',
                                  'yellow', 'red']]
        self.game_board.rowHeights = [1, 0, 0, 0, 0, 0, 0]
        self.game_board.remaining_moves = 1
        self.game_board.validate_move(1, 0)
        self.assertEqual(self.game_board.game_result,
                         'draw')

    def test_move_after_draw(self):
        # Checks if game discards move after a draw and returns right error
        self.game_board.board = [[0, 'red', 'yellow', 'red', 'yellow',
                                 'yellow', 'red'],
                                 ['red', 'red', 'yellow', 'red', 'yellow',
                                  'red', 'red'],
                                 ['yellow', 'yellow', 'red', 'yellow', 'red',
                                  'yellow', 'yellow'],
                                 ['yellow', 'red', 'red', 'yellow', 'red',
                                  'red', 'yellow'],
                                 ['yellow', 'red', 'yellow', 'red', 'yellow',
                                  'red', 'yellow'],
                                 ['red', 'yellow', 'red', 'yellow', 'red',
                                  'yellow', 'red']]
        self.game_board.rowHeights = [1, 0, 0, 0, 0, 0, 0]
        self.game_board.remaining_moves = 1
        self.game_board.validate_move(1, 0)
        self.assertEqual(self.game_board.validate_move(2, 0),
                         'No more remaining moves')

    def test_move_in_filled_column(self):
        # Checks if game discards move on full col and returns correct error
        player = 1
        for i in range(6):
            self.game_board.validate_move(player, 1)
            player = 2 if player == 1 else 1
        self.assertEqual(self.game_board.validate_move(player, 1),
                         'Column is already full')

    def tearDown(self):
        self.game_board = None
        db.clear()


if __name__ == '__main__':
    unittest.main()
