from piece import Men
from piece import King
import time


class Board:
    def __init__(self, cols, rows):
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.turn = 'white'
        self.extra_atack = None
        self.p1Name = "Player 1"
        self.p2Name = "Player 2"
        self.p1Time = 300
        self.p2Time = 300
        self.p1PrevTime = self.p1Time
        self.p2PrevTime = self.p2Time
        self.winner = None
        self.must_atack = False
        self.ready = False
        self.start_time = 0
        self.moves_list = []

        self.board[1][0] = Men('black')
        self.board[3][0] = Men('black')
        self.board[5][0] = Men('black')
        self.board[7][0] = Men('black')

        self.board[0][1] = Men('black')
        self.board[2][1] = Men('black')
        self.board[4][1] = Men('black')
        self.board[6][1] = Men('black')

        self.board[1][2] = Men('black')
        self.board[3][2] = Men('black')
        self.board[5][2] = Men('black')
        self.board[7][2] = Men('black')

        self.board[0][5] = Men('white')
        self.board[2][5] = Men('white')
        self.board[4][5] = Men('white')
        self.board[6][5] = Men('white')

        self.board[3][6] = Men('white')
        self.board[1][6] = Men('white')
        self.board[5][6] = Men('white')
        self.board[7][6] = Men('white')

        self.board[0][7] = Men('white')
        self.board[2][7] = Men('white')
        self.board[4][7] = Men('white')
        self.board[6][7] = Men('white')

        self.update_moves()

    def make_move(self, start_c, start_r, c, r):
        start_cell = self.board[start_c][start_r]
        if not self.must_atack and start_cell != 0 and \
                (start_c, start_r, c, r) in start_cell.moves and \
                self.turn == start_cell.get_color():
            self.board[c][r] = self.board[start_c][start_r]
            self.board[start_c][start_r] = 0
            self.change_turn()
            self.check_king()
            self.update_moves()
            self.moves_list.append(f'{start_c}{start_r}{c}{r}')

    def make_atack(self, start_c, start_r, c, r):
        start_cell = self.board[start_c][start_r]
        if self.must_atack and start_cell != 0 and \
                (start_c, start_r, c, r) in start_cell.atacks and \
                (self.extra_atack is None or
                self.extra_atack == (start_c, start_r)) and \
                self.turn == start_cell.get_color():
            self.board[c][r] = self.board[start_c][start_r]
            self.board[start_c][start_r] = 0
            self.clear_diag(start_c, start_r, c, r)
            self.check_winner()
            self.check_king()
            self.board[c][r].valid_atacks(c, r, self.board)
            if self.board[c][r].atacks == set():
                self.change_turn()
                self.extra_atack = None
            else:
                self.extra_atack = (c, r)
            self.update_moves()
            self.moves_list.append(f'{start_c}{start_r}{c}{r}')

    def change_turn(self):
        self.start_time = time.time()
        if self.turn == 'white':
            self.turn = 'black'
            self.p1PrevTime = self.p1Time
        else:
            self.turn = 'white'
            self.p2PrevTime = self.p2Time

    def clear_diag(self, start_c, start_r, finish_c, finish_r):
        # DOWN_RIGHT
        if finish_c > start_c and finish_r > start_r:
            while start_c < (finish_c - 1):
                start_c += 1
                start_r += 1
                self.board[start_c][start_r] = 0
        # DOWN_LEFT
        elif finish_c < start_c and finish_r > start_r:
            while start_c > (finish_c + 1):
                start_c -= 1
                start_r += 1
                self.board[start_c][start_r] = 0
        # UP_LEFT
        elif finish_c < start_c and finish_r < start_r:
            while start_c > (finish_c + 1):
                start_c -= 1
                start_r -= 1
                self.board[start_c][start_r] = 0
        # UP_RIGHT
        elif finish_c > start_c and finish_r < start_r:
            while start_c < (finish_c - 1):
                start_c += 1
                start_r -= 1
                self.board[start_c][start_r] = 0
        else:
            print('[ERROR] Wrong data in clear_diag()')

    def must_to_atack(self):
        for col in self.board:
            for cell in col:
                if cell != 0 and cell.get_color() == self.turn and \
                        cell.atacks != set():
                    self.must_atack = True
                    return None
        self.must_atack = False

    def check_king(self):
        for c, col in enumerate(self.board):
            if col[7] != 0 and col[7].get_color() == 'black' and \
                    col[7].get_type() == 'men':
                self.board[c][7] = King('black')
                if self.extra_atack is not None:
                    self.extra_atack = (c, 7)
        for c, col in enumerate(self.board):
            if col[0] != 0 and col[0].get_color() == 'white' and \
                    col[0].get_type() == 'men':
                self.board[c][0] = King('white')
                if self.extra_atack is not None:
                    self.extra_atack = (c, 0)

    def check_winner(self):
        count_white, count_black, winner = 0, 0, 0
        for col in self.board:
            for cell in col:
                if cell != 0:
                    winner = cell
                    if cell.get_color() == 'white':
                        count_white += 1
                    else:
                        count_black += 1
                if min(count_white, count_black) > 0:
                    return None
        self.winner = winner.get_color()

    def update_moves(self):
        for c, col in enumerate(self.board):
            for r, cell in enumerate(col):
                if cell != 0:
                    cell.valid_atacks(c, r, self.board)
                    cell.valid_moves(c, r, self.board)

        self.must_to_atack()
