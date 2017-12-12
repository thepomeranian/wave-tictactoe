from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from random import randint, choice
import re

app = Flask(__name__)
api = Api(app)


class tictactoe(Resource):

    def get(self):
        board = request.args.get('board')
        if self.validify(board):
            if self.who_turn(board) is 'o':
                board = self.take_turn(board)
            return {'board': board}
        else:
            return {'empty': 'very empty'}

    def validify(self, board):
        """Verify's this is a valid board
        Checks for a winner
        Checks if board has less than 9 characters or empty
        """
        o_spaces = [iterator for iterator,
                    item in enumerate(board) if item == 'o']
        x_spaces = [iterator for iterator,
                    item in enumerate(board) if item == 'x']
        if board is None:
            return False
        if len(board) > 9 or len(board) < 9:
            return False
        if self.is_winning_combo(board):
            print 'there is a winner'
            return False
        if (len(o_spaces) - len(x_spaces)) > 1 or (len(x_spaces) - len(o_spaces)) > 1:
            return False
        return True

    def is_winning_combo(self, board):
        winning_combos = [[6, 7, 8], [3, 4, 5], [0, 1, 2], [0, 3, 6], [1, 4, 7], [2, 5, 8],
                          [0, 4, 8], [2, 4, 6]]
        for combo in winning_combos:
            if (board[combo[0]] == board[combo[1]] == board[combo[2]] == 'x'):
                return True
            if (board[combo[0]] == board[combo[1]] == board[combo[2]] == 'o'):
                return True
        return False

    def who_turn(self, board):
        """Assumes that it's always server's turn if using API"""
        return 'o'

    def take_turn(self, board):
        """Allows the server to make a random move
        """
        # if the board is empty, choose a random space
        if board.isspace():
            new_board = list(board)
            turn = randint(0, 8)
            new_board[turn] = 'o'
            return ''.join(new_board)
        new_board = list(board)
        # currently using choice since there's no logic
        turn = choice(self.find_empty(board))
        # double check that the space is empty and mark it with 'o'
        if new_board[turn] == ' ':
            new_board[turn] = 'o'
            new_board = ''.join(new_board)
            # checks if this is the winning move
            if self.is_winning_combo(new_board) or self.is_winning_combo(new_board):
              print 'winning move'
            return new_board
        else:
            self.take_turn(board)

    def find_empty(self, board):
        """Finds empty spaces on board
        TODO: add logic that chooses the best space on the board
        give each move a score (how close it gets to a winning combo)
        rank each move and return the highest ranked move
        """
        new_board = list(board)
        empty_spaces = [iterator for iterator,
                        item in enumerate(new_board) if not item.isalpha()]
        return empty_spaces

api.add_resource(tictactoe, '/')

if __name__ == '__main__':
    app.run(debug=True)