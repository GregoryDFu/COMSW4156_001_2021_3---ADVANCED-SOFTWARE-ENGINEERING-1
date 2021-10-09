import sqlite3
from sqlite3 import Error

'''
Initializes the Table GAME
Do not modify
'''


def init_db():
    # creates Table
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute('CREATE TABLE GAME(current_turn TEXT, board TEXT,' +
                     'winner TEXT, player1 TEXT, player2 TEXT' +
                     ', remaining_moves INT, row_heights TEXT)')
        print('Database Online, table created')
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


'''
move is a tuple (current_turn, board, winner, player1, player2,
remaining_moves, row_heights)
Insert Tuple into table
'''


def add_move(move):  # will take in a tuple
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        query = '''INSERT INTO GAME(current_turn, board, winner,
                    player1, player2, remaining_moves, row_heights)
                    VALUES(?,?,?,?,?,?,?)'''
        c = conn.cursor()
        c.execute(query, move)
        conn.commit()
        c.close()
        return True
    except Error as e:
        print(e)
        return False
    finally:
        if conn:
            conn.close()


'''
Get the last move played
return (current_turn, board, winner, player1, player2, remaining_moves)
'''


def getMove():
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM GAME')
        count = c.fetchone()
        if count[0] == 0:
            return None
        query = '''SELECT * FROM GAME WHERE remaining_moves =
                    (SELECT MIN(remaining_moves) FROM GAME)'''
        c.execute(query)
        res = c.fetchone()
        c.close()
        return res
    except Error as e:
        print(e)
        return None
    finally:
        if conn:
            conn.close()


'''
Clears the Table GAME
Do not modify
'''


def clear():
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute("DROP TABLE GAME")
        print('Database Cleared')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()
