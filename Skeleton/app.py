from flask import Flask, render_template, request, redirect, jsonify
from json import dump
from Gameboard import Gameboard
import db

app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

game = None
p1_color = None
'''
Implement '/' endpoint
Method Type: GET
return: template player1_connect.html and status = "Pick a Color."
Initial Webpage where gameboard is initialized
'''


@app.route('/', methods=['GET'])
def player1_connect():
    return render_template("player1_connect.html", status = "Pick a Color.")


'''
Helper function that sends to all boards don't modify
'''


@app.route('/autoUpdate', methods=['GET'])
def updateAllBoards():
    try:
        return jsonify(move=game.board, winner=game.game_result,
                       color=game.player1)
    except Exception:
        return jsonify(move="")


'''
Implement '/p1Color' endpoint
Method Type: GET
return: template player1_connect.html and status = <Color picked>
Assign player1 their color
'''


@app.route('/p1Color', methods=['GET'])
def player1_config():
    global game
    game = Gameboard()
    global p1_color
    p1_color = request.args.get("color")
    game.player1 = p1_color
    return render_template("player1_connect.html", status=p1_color)


'''
Implement '/p2Join' endpoint
Method Type: GET
return: template p2Join.html and status = <Color picked> or Error
if P1 didn't pick color first

Assign player2 their color
'''


@app.route('/p2Join', methods=['GET'])
def p2Join():
    if p1_color is None:
        raise Exception("P1 has not picked a color")
    else:
        if p1_color == "yellow":
            p2_color = "red"
        else:
            p2_color = "yellow"
        game.player2 = p2_color
        return render_template("p2Join.html", status=p2_color)


'''
Implement '/move1' endpoint
Method Type: POST
return: jsonify (move=<CurrentBoard>,
invalid=True or False, winner = <currWinner>)
If move is valid --> invalid = False else invalid = True
If invalid == True, also return reason= <Why Move is Invalid>

Process Player 1's move
'''


@app.route('/move1', methods=['POST'])
def p1_move():
    resp = game.handle_move(1, request.get_json())
    is_valid = True if resp == "pass" else False
    return jsonify(move=game.board, invalid=not is_valid, reason=resp, winner=game.game_result)

'''
Same as '/move1' but instead proccess Player 2
'''


@app.route('/move2', methods=['POST'])
def p2_move():
    resp = game.handle_move(2, request.get_json())
    is_valid = True if resp == "pass" else False
    return jsonify(move=game.board, invalid=not is_valid, reason=resp, winner=game.game_result)



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
