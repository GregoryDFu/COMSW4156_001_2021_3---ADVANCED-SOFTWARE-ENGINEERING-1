import unittest
import db


class Test_Testdb(unittest.TestCase):
    def setUp(self):
        db.init_db()

    def test_valid_add_move(self):
        # Test add move with a valid tuple
        move = (('p2',
                 "[[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], \
                   [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], \
                   ['red', 0, 0, 0, 0, 0, 0]]",
                 '', 'red', 'yellow', 41,
                 '[5, 6, 6, 6, 6, 6, 6]'))
        self.assertEqual(db.add_move(move), True)

    def test_invalid_add_move(self):
        # Test add move with an invalid tuple
        move = (('p2',
                 "[[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], \
                   [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], \
                   ['red', 0, 0, 0, 0, 0, 0]]",
                 '', 'red', 'yellow',
                 '[5, 6, 6, 6, 6, 6, 6]'))
        self.assertEqual(db.add_move(move), False)

    def test_valid_get_move(self):
        # Test that get move returns a tuple with the appropriate data
        move = (('p2',
                 "[[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], \
                   [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], \
                   ['red', 0, 0, 0, 0, 0, 0]]",
                 '', 'red', 'yellow', 41,
                 '[5, 6, 6, 6, 6, 6, 6]'))
        print(db.add_move(move))
        res = db.getMove()
        self.assertEqual(res[0], 'p2')
        self.assertEqual(res[1], '[[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], \
                   [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], \
                   [\'red\', 0, 0, 0, 0, 0, 0]]')
        self.assertEqual(res[2], '')
        self.assertEqual(res[3], 'red')
        self.assertEqual(res[4], 'yellow')
        self.assertEqual(res[5], 41)
        self.assertEqual(res[6], '[5, 6, 6, 6, 6, 6, 6]')

    def test_empty_get_move(self):
        # Test that get move on empty db returns None
        self.assertEqual(db.getMove(), None)

    def test_get_move_gets_last_move(self):
        # Test that get move gets the latest move in the db
        move1 = (('p1',
                 "[[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], \
                   [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], \
                   [0, 0, 0, 0, 0, 0, 0]]",
                  '', 'red', 'yellow', 42,
                  '[6, 6, 6, 6, 6, 6, 6]'))
        db.add_move(move1)
        move2 = (('p2',
                 "[[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], \
                   [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], \
                   ['red', 0, 0, 0, 0, 0, 0]]",
                  '', 'red', 'yellow', 41,
                  '[5, 6, 6, 6, 6, 6, 6]'))
        db.add_move(move2)
        res = db.getMove()
        self.assertEqual(res[0], 'p2')
        self.assertEqual(res[1], '[[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], \
                   [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], \
                   [\'red\', 0, 0, 0, 0, 0, 0]]')
        self.assertEqual(res[2], '')
        self.assertEqual(res[3], 'red')
        self.assertEqual(res[4], 'yellow')
        self.assertEqual(res[5], 41)
        self.assertEqual(res[6], '[5, 6, 6, 6, 6, 6, 6]')

    def tearDown(self):
        db.clear()


if __name__ == '__main__':
    unittest.main()
