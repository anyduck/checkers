class Piece:
    def __init__(self, color):
        self.color = color
        self.image = None
        self.moves, self.atacks = set(), set()

    def get_color(self):
        return self.color

    def get_type(self):
        return self.type


class Men(Piece):
    def __init__(self, color):
        super().__init__(color)
        if self.color == 'white':
            self.image = 0
        else:
            self.image = 2
        self.type = 'men'

    def valid_moves(self, start_c, start_r, board_data):
        self.moves = set()
        if self.color == 'white':
            if start_c < 7 and board_data[start_c + 1][start_r - 1] == 0:
                self.moves.add((start_c, start_r, start_c + 1, start_r - 1))
            if min(start_c, start_r) > 0 and board_data[start_c - 1][start_r - 1] == 0:
                self.moves.add((start_c, start_r, start_c - 1, start_r - 1))
        else:
            if max(start_c, start_r) < 7 and board_data[start_c + 1][start_r + 1] == 0:
                self.moves.add((start_c, start_r, start_c + 1, start_r + 1))
            if start_c > 0 and board_data[start_c - 1][start_r + 1] == 0:
                self.moves.add((start_c, start_r, start_c - 1, start_r + 1))

    def valid_atacks(self, start_c, start_r, board_data):
        self.atacks = set()
        if self.color == 'white':
            # UP_RIGHT
            if start_c < 6 and start_r > 1 and board_data[start_c + 2][start_r - 2] == 0 and board_data[start_c + 1][start_r - 1] != 0 and board_data[start_c + 1][start_r - 1].get_color() == 'black':
                self.atacks.add((start_c, start_r, start_c + 2, start_r - 2))
            # UP_LEFT
            if start_c > 1 and start_r > 1 and board_data[start_c - 2][start_r - 2] == 0 and board_data[start_c - 1][start_r - 1] != 0 and board_data[start_c - 1][start_r - 1].get_color() == 'black':
                self.atacks.add((start_c, start_r, start_c - 2, start_r - 2))
            # DOWN_RIGHT
            if start_c < 6 and start_r < 6 and board_data[start_c + 2][start_r + 2] == 0 and board_data[start_c + 1][start_r + 1] != 0 and board_data[start_c + 1][start_r + 1].get_color() == 'black':
                self.atacks.add((start_c, start_r, start_c + 2, start_r + 2))
            # DOWN_LEFT
            if start_c > 1 and start_r < 6 and board_data[start_c - 2][start_r + 2] == 0 and board_data[start_c - 1][start_r + 1] != 0 and board_data[start_c - 1][start_r + 1].get_color() == 'black':
                self.atacks.add((start_c, start_r, start_c - 2, start_r + 2))
        else:
            # UP_RIGHT
            if start_c < 6 and start_r > 1 and board_data[start_c + 2][start_r - 2] == 0 and board_data[start_c + 1][start_r - 1] != 0 and board_data[start_c + 1][start_r - 1].get_color() == 'white':
                self.atacks.add((start_c, start_r, start_c + 2, start_r - 2))
            # UP_LEFT
            if start_c > 1 and start_r > 1 and board_data[start_c - 2][start_r - 2] == 0 and board_data[start_c - 1][start_r - 1] != 0 and board_data[start_c - 1][start_r - 1].get_color() == 'white':
                self.atacks.add((start_c, start_r, start_c - 2, start_r - 2))
            # DOWN_RIGHT
            if start_c < 6 and start_r < 6 and board_data[start_c + 2][start_r + 2] == 0 and board_data[start_c + 1][start_r + 1] != 0 and board_data[start_c + 1][start_r + 1].get_color() == 'white':
                self.atacks.add((start_c, start_r, start_c + 2, start_r + 2))
            # DOWN_LEFT
            if start_c > 1 and start_r < 6 and board_data[start_c - 2][start_r + 2] == 0 and board_data[start_c - 1][start_r + 1] != 0 and board_data[start_c - 1][start_r + 1].get_color() == 'white':
                self.atacks.add((start_c, start_r, start_c - 2, start_r + 2))


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        if self.color == 'white':
            self.image = 1
        else:
            self.image = 3
        self.type = 'king'

    def valid_moves(self, start_c, start_r, board_data):
        self.moves = set()
        min_coord = min(start_c, start_r)
        max_coord = max(start_c, start_r)
        # UP_LEFT
        i = 0
        while (min_coord - i) > 0:
            i += 1
            if board_data[start_c - i][start_r - i] == 0:
                self.moves.add((start_c, start_r, start_c - i, start_r - i))
            else:
                break

        # DOWN_RIGHT
        i = 0
        while (max_coord + i) < 7:
            i += 1
            if board_data[start_c + i][start_r + i] == 0:
                self.moves.add((start_c, start_r, start_c + i, start_r + i))
            else:
                break

        # DOWN_LEFT
        i = 0
        while (start_r + i) < 7 and (start_c - i) > 0:
            i += 1
            if board_data[start_c - i][start_r + i] == 0:
                self.moves.add((start_c, start_r, start_c - i, start_r + i))
            else:
                break

        # UP_RIGHT
        i = 0
        while (start_r - i) > 0 and (start_c + i) < 7:
            i += 1
            if board_data[start_c + i][start_r - i] == 0:
                self.moves.add((start_c, start_r, start_c + i, start_r - i))
            else:
                break

    def valid_atacks(self, start_c, start_r, board_data):
        self.atacks = set()
        min_coord = min(start_c, start_r)
        max_coord = max(start_c, start_r)

        # UP_LEFT
        i = 0
        target = False
        while (min_coord - i) > 1:
            i += 1
            cell = board_data[start_c - i][start_r - i]
            if cell == 0:
                pass
            elif cell.get_color() == self.color:
                break
            else:
                target = True
                break

        while target and (min_coord - i) > 0:
            i += 1
            if board_data[start_c - i][start_r - i] == 0:
                self.atacks.add((start_c, start_r, start_c - i, start_r - i))
            else:
                break

        # DOWN_RIGHT
        i = 0
        target = False
        while (max_coord + i) < 6:
            i += 1
            cell = board_data[start_c + i][start_r + i]
            if cell == 0:
                pass
            elif cell.get_color() == self.color:
                break
            else:
                target = True
                break

        while target and (max_coord + i) < 7:
            i += 1
            if board_data[start_c + i][start_r + i] == 0:
                self.atacks.add((start_c, start_r, start_c + i, start_r + i))
            else:
                break

        # DOWN_LEFT
        i = 0
        target = False
        while (start_c - i) > 1 and (start_r + i) < 6:
            i += 1
            cell = board_data[start_c - i][start_r + i]
            if cell == 0:
                pass
            elif cell.get_color() == self.color:
                break
            else:
                target = True
                break

        while target and (start_c - i) > 0 and (start_r + i) < 7:
            i += 1
            if board_data[start_c - i][start_r + i] == 0:
                self.atacks.add((start_c, start_r, start_c - i, start_r + i))
            else:
                break

        # UP_RIGHT
        i = 0
        target = False
        while (start_c + i) < 6 and (start_r - i) > 1:
            i += 1
            cell = board_data[start_c + i][start_r - i]
            if cell == 0:
                pass
            elif cell.get_color() == self.color:
                break
            else:
                target = True
                break

        while target and (start_c + i) < 7 and (start_r - i) > 0:
            i += 1
            if board_data[start_c + i][start_r - i] == 0:
                self.atacks.add((start_c, start_r, start_c + i, start_r - i))
            else:
                break
