'''
Checkers v1.3 Muliplayer game by @moodduckk
'''

import pygame
import os
import sys
from client import Network


class Game():
    def __init__(self, name, n):
        pygame.init()
        pygame.font.init()

        self.color = n.board.start_user
        self.n = n
        self.bo = self.n.send("name " + name)
        self.prevBoard = self.bo

        self.images = [
            pygame.image.load(self.resource_path('images\\men_white.png')),
            pygame.image.load(self.resource_path('images\\king_white.png')),
            pygame.image.load(self.resource_path('images\\men_black.png')),
            pygame.image.load(self.resource_path('images\\king_black.png'))
            ]

        self.SQUARE_SIDE = 70
        self.OFFSET = self.SQUARE_SIDE // 2
        self.FPS = 30
        self.FIRST_COLOR = (255, 255, 255)     # White
        self.SECOND_COLOR = (140, 184, 219)    # Blue light
        self.SCREEN = pygame.display.set_mode((self.SQUARE_SIDE*8, self.SQUARE_SIDE*9), pygame.RESIZABLE)
        self.LARGE_FONT = pygame.font.Font(self.resource_path('fonts\\Segoe UI Italic.ttf'), 45)
        self.SMALL_FONT = pygame.font.Font(self.resource_path('fonts\\Segoe UI Italic.ttf'), 21)
        self.SMALL_BOLD_FONT = pygame.font.Font(self.resource_path('fonts\\Segoe UI Bold Italic.ttf'), 21)
        self.IMAGES = [pygame.transform.scale(image, (self.SQUARE_SIDE, self.SQUARE_SIDE)) for image in self.images]

        pygame.display.set_icon(pygame.image.load(self.resource_path('images\\icon.png')))
        pygame.display.set_caption('Checkers')
        self.clock = pygame.time.Clock()
        self.rotate = True
        self.animate = False

    # Get absolute path to resource, works for dev and for PyInstaller
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    # Rotate board for black player
    def rotate_board(self):
        self.bo.board = self.bo.board[::-1]
        for c, col in enumerate(self.bo.board):
            self.bo.board[c] = col[::-1]
        self.rotate = False

    def reverse_coords(self, c, r):
        return abs(c-7), abs(r-7)

    def reverse_check_coord(self, coord):
        if self.color == 'white':
            return coord
        else:
            return abs(coord-7)

    def start_animation(self):
        if (self.bo.moves_list != [] and not self.animate and
                self.prevBoard.turn != self.color and
                self.bo.turn != self.prevBoard.turn) or (

                self.bo.extra_atack is not None and
                self.bo.turn != self.color and
                self.bo.extra_atack != self.prevBoard.extra_atack
                ):
            self.anim_c = self.reverse_check_coord(int(self.bo.moves_list[-1][0]))
            self.anim_r = self.reverse_check_coord(int(self.bo.moves_list[-1][1]))
            self.end_anim_c = self.reverse_check_coord(int(self.bo.moves_list[-1][2]))
            self.end_anim_r = self.reverse_check_coord(int(self.bo.moves_list[-1][3]))
            self.animate = True
            self.anim_x = self.anim_c*self.SQUARE_SIDE
            self.anim_y = self.anim_r*self.SQUARE_SIDE + self.OFFSET
            self.end_anim_x = self.end_anim_c*self.SQUARE_SIDE
            self.end_anim_y = self.end_anim_r*self.SQUARE_SIDE + self.OFFSET
            delta_x = self.end_anim_x - self.anim_x
            delta_y = self.end_anim_y - self.anim_y
            if delta_x > 0:
                if delta_y > 0:
                    self.anim_type = 4
                else:
                    self.anim_type = 1
            else:
                if delta_y > 0:
                    self.anim_type = 3
                else:
                    self.anim_type = 2

    # Draw whole window
    def redraw_board(self, win):
        win.fill(self.FIRST_COLOR)
        c, c0, r0 = 0, 0, 0
        low_square = self.SQUARE_SIDE // 10

        # Draw timer bar
        p1TimeY = self.OFFSET - 2*low_square
        p2TimeY = self.OFFSET + 8*self.SQUARE_SIDE

        if self.color == 'black':
            p1TimeY, p2TimeY = p2TimeY, p1TimeY

        pygame.draw.rect(win, (0, 0, 0), (0, p1TimeY, int(self.bo.p2Time/75*2*self.SQUARE_SIDE), 2*low_square))
        pygame.draw.rect(win, (0, 0, 0), (0, p2TimeY, 8*self.SQUARE_SIDE, 2*low_square))
        pygame.draw.rect(win, self.FIRST_COLOR, (0, p2TimeY, int(self.bo.p1Time/75*2*self.SQUARE_SIDE), 2*low_square))

        # Draw border grid
        for c in range(89):
            r0 = c % 2 * low_square
            c0 = c*low_square
            pygame.draw.rect(win, self.SECOND_COLOR, (c0, self.OFFSET + self.SQUARE_SIDE*8 + r0, low_square, low_square))
            pygame.draw.rect(win, self.SECOND_COLOR, (c0, self.OFFSET - low_square - r0, low_square, low_square))

        if self.animate:
            temp_board = self.prevBoard.board
        else:
            temp_board = self.bo.board

        # Draw board grid, pieces
        for c, col in enumerate(temp_board):
            for r, cell in enumerate(col):
                c0 = c*self.SQUARE_SIDE
                r0 = r*self.SQUARE_SIDE

                # Draw board grid
                if (c % 2 == 0) ^ (r % 2 == 0):
                    pygame.draw.rect(win, self.SECOND_COLOR, (c0, r0 + self.OFFSET, self.SQUARE_SIDE, self.SQUARE_SIDE))

                # Draw pieces
                if cell != 0:
                    if (self.selected is None or (c, r) != self.selected[0]) and \
                            (not self.animate or not (self.anim_c, self.anim_r) == (c, r)):
                        win.blit(self.IMAGES[cell.image], (c0, r0 + self.OFFSET))

        # Draw selected piece
        if self.selected is not None:
            win.blit(self.IMAGES[self.selected[1].image], (self.pointer_x, self.pointer_y))

        # Draw animated piece
        if self.animate:
            if self.anim_type == 1 and self.end_anim_x > self.anim_x:
                self.anim_x += self.SQUARE_SIDE/5
                self.anim_y -= self.SQUARE_SIDE/5
                win.blit(self.IMAGES[self.bo.board[self.end_anim_c][self.end_anim_r].image], (int(self.anim_x), int(self.anim_y)))
            elif self.anim_type == 2 and self.end_anim_x < self.anim_x:
                self.anim_x -= self.SQUARE_SIDE/5
                self.anim_y -= self.SQUARE_SIDE/5
                win.blit(self.IMAGES[self.bo.board[self.end_anim_c][self.end_anim_r].image], (int(self.anim_x), int(self.anim_y)))
            elif self.anim_type == 3 and self.end_anim_x < self.anim_x:
                self.anim_x -= self.SQUARE_SIDE/5
                self.anim_y += self.SQUARE_SIDE/5
                win.blit(self.IMAGES[self.bo.board[self.end_anim_c][self.end_anim_r].image], (int(self.anim_x), int(self.anim_y)))
            elif self.anim_type == 4 and self.end_anim_x > self.anim_x:
                self.anim_x += self.SQUARE_SIDE/5
                self.anim_y += self.SQUARE_SIDE/5
                win.blit(self.IMAGES[self.bo.board[self.end_anim_c][self.end_anim_r].image], (int(self.anim_x), int(self.anim_y)))
            else:
                self.animate = False
                win.blit(self.IMAGES[self.bo.board[self.end_anim_c][self.end_anim_r].image], (self.end_anim_x, self.end_anim_y))
                self.prevBoard = self.bo

        # Draw text
        if self.bo.ready:
            color_info = self.SMALL_BOLD_FONT.render('YOU ARE ' + self.color.upper(), True, (0, 0, 0))
            win.blit(color_info, (int(self.SQUARE_SIDE*4 - color_info.get_width()/2), int(8.85*self.SQUARE_SIDE - color_info.get_height()*0.52)))
            turn_info = self.SMALL_BOLD_FONT.render(self.bo.turn.upper() + ' TURN', True, (0, 0, 0))
            win.blit(turn_info, (int(self.SQUARE_SIDE*4 - turn_info.get_width()/2), int(self.OFFSET*0.5 - low_square - turn_info.get_height()*0.52)))

            p2Time = self.SMALL_FONT.render(f"{self.bo.p2Name}'s time: %02d:%02d" % divmod(self.bo.p2Time, 60), True, (0, 0, 0))
            p1Time = self.SMALL_FONT.render(f"{self.bo.p1Name}'s time: %02d:%02d" % divmod(self.bo.p1Time, 60), True, (0, 0, 0))

            p1Y = int(8.85*self.SQUARE_SIDE - p1Time.get_height()*0.52)
            p2Y = int(self.OFFSET*0.5 - low_square - p2Time.get_height()*0.52)

            if self.color == 'black':
                p1Y, p2Y = p2Y, p1Y

            win.blit(p1Time, (int(self.SQUARE_SIDE*8 - p1Time.get_width() - 5), p1Y))
            win.blit(p2Time, (int(self.SQUARE_SIDE*8 - p2Time.get_width() - 5), p2Y))
        else:
            game_info = self.LARGE_FONT.render('Waiting for other players...', True, (0, 0, 0))
            win.blit(game_info, (int(self.SQUARE_SIDE*4 - game_info.get_width()/2), int(self.OFFSET + self.SQUARE_SIDE*4 - game_info.get_height()/2)))

    def multiplayer(self):
        # Some varible declaration
        running = True
        dragging, event_break, self.pointer_x, self.pointer_y = False, False, False, False
        self.selected = None
        count = 0

        # Start main game loop
        while running:

            # Request board from server
            if count == int(self.FPS/4):
                temp_board = self.bo
                self.bo = self.n.send("get")

                # Check oponent's status
                if self.bo is None:
                    print('[ERROR] Other player left')
                    self.end_screen('Other player left')
                    break

                elif self.bo.extra_atack is not None and \
                        self.bo.turn != self.color and \
                        self.bo.extra_atack != self.prevBoard.extra_atack:
                    self.animate = False
                    self.prevBoard = temp_board
                self.rotate = True
                count = 0
            else:
                count += 1

            # Check is game over
            if self.bo.winner == "white":
                self.end_screen("White is the Winner!")
                break
            elif self.bo.winner == "black":
                self.end_screen("Black is the winner")
                break

            # Event pull
            for event in pygame.event.get():

                # Quit from app
                if event.type == pygame.QUIT:
                    self.n.disconnect()
                    running = False
                    pygame.font.quit()
                    pygame.quit()
                    event_break = True
                    break

                # Resize window
                elif event.type == pygame.VIDEORESIZE:
                    if self.SCREEN.get_height() != event.h:
                        self.resize_screen(int(event.h/9))
                    elif self.SCREEN.get_width() != event.w:
                        self.resize_screen(int(event.w/8))

                # Press mouse button
                elif event.type == pygame.MOUSEBUTTONDOWN and self.bo.ready:
                    mous_x, mous_y = event.pos
                    start_c, start_r = int(mous_x/self.SQUARE_SIDE), int((mous_y - self.OFFSET)/self.SQUARE_SIDE)
                    if mous_y >= self.OFFSET and start_r <= 7:
                        piece = self.bo.board[start_c][start_r]
                        if piece != 0 and self.color == self.bo.turn and piece.color == self.color:
                            dragging = True
                            self.selected = ((start_c, start_r), piece)
                            start_x, start_y = start_c*self.SQUARE_SIDE, start_r*self.SQUARE_SIDE + self.OFFSET
                            self.pointer_x, self.pointer_y = start_x, start_y
                            offset_x, offset_y = mous_x - start_x, mous_y - start_y

                # Mouse motion
                elif event.type == pygame.MOUSEMOTION and dragging:
                    mous_x, mous_y = event.pos
                    self.pointer_x, self.pointer_y = mous_x - offset_x, mous_y - offset_y

                # Release mouse button
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragging and piece.color == self.bo.turn and self.color == self.bo.turn:
                        mous_x, mous_y = event.pos
                        finish_c = int((mous_x - offset_x)/self.SQUARE_SIDE + 0.5)
                        finish_r = int((mous_y - offset_y - self.OFFSET)/self.SQUARE_SIDE + 0.5)
                        if self.color == 'black':
                            finish_c, finish_r = self.reverse_coords(finish_c, finish_r)
                            start_c, start_r = self.reverse_coords(start_c, start_r)
                            self.rotate = True
                        if self.bo.must_atack:
                            self.bo = self.n.send(f"atack {start_c} {start_r} {finish_c} {finish_r}")
                            self.animate = False
                            if self.bo.turn != self.color:
                                self.prevBoard = self.bo
                        else:
                            self.bo = self.n.send(f"move {start_c} {start_r} {finish_c} {finish_r}")
                            self.animate = False
                            if self.bo.turn != self.color:
                                self.prevBoard = self.bo
                    dragging = False
                    self.selected = None

                elif event.type == pygame.KEYDOWN:
                    if event.key == 112:
                        print(self.bo.moves_list)

            if event_break: break
            if self.rotate and self.color == 'black': self.rotate_board()
            self.start_animation()

            self.redraw_board(self.SCREEN)
            pygame.display.update()
            self.clock.tick(self.FPS)

    def resize_screen(self, square_side_len):
        self.SQUARE_SIDE = square_side_len
        self.SCREEN = pygame.display.set_mode((square_side_len*8, square_side_len*9), pygame.RESIZABLE)
        self.OFFSET = int(square_side_len/2)
        self.LARGE_FONT = pygame.font.Font(self.resource_path('fonts\\Segoe UI Italic.ttf'), int(square_side_len*0.65))
        self.SMALL_FONT = pygame.font.Font(self.resource_path('fonts\\Segoe UI Italic.ttf'), int(square_side_len*0.3))
        self.SMALL_BOLD_FONT = pygame.font.Font(self.resource_path('fonts\\Segoe UI Bold Italic.ttf'), int(square_side_len*0.3), bold=True)
        self.IMAGES = [pygame.transform.scale(image, (square_side_len, square_side_len)) for image in self.images]

    def end_screen(self, text):
        self.n.disconnect()
        txt = self.LARGE_FONT.render(text, 1, (0, 0, 0))
        self.SCREEN.fill(self.FIRST_COLOR)
        self.SCREEN.blit(txt, (int(self.SQUARE_SIDE*4 - txt.get_width()/2),
                               int(self.SQUARE_SIDE*4.5 - txt.get_height()/2)))
        pygame.display.update()

        pygame.time.set_timer(pygame.USEREVENT+1, 3000)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                        event.type == pygame.KEYDOWN or \
                        event.type == pygame.USEREVENT+1:
                    running = False
                    pygame.font.quit()
                    pygame.quit()
                    break

if __name__ == "__main__":
    def connect():
        global n
        n = Network()
        return n

    name = input('Enter your name:')

    try:
        bo = connect()
        game = Game(name, bo)
        game.multiplayer()
    except Exception as e:
        print('[ERROR] ', e)
        print('Server Offline')
