'''
Checkers v1.0 Muliplayer game by @moodduckk
'''


import pygame
import time
import pickle
import socket
import os
from client import Network


pygame.init()


def main(win):
    global n
    # Some varible declaration
    running = True
    dragging, pointer_x, pointer_y = False, False, False
    bo = n.send("name " + name)
    color = bo.start_user
    selected = None
    count = 0

    # Add zero before number if needed
    def normalize(norm):
        norm = int(norm)
        if norm >= 10:
            return str(norm)
        else:
            return '0' + str(norm)

    # Draw whole window
    def refresh_board():
        win.fill(FIRST_COLOR)
        c, c0, r0 = 0, 0, 0
        low_square = int(SQUARE_SIDE/10)
        pointer_c = int(pointer_x/SQUARE_SIDE + 0.5)
        pointer_r = int((pointer_y - OFFSET)/SQUARE_SIDE + 0.5)

        # Draw border grid
        while c0 < SQUARE_SIDE*8:
            if c % 2 == 0:
                r0 = 0
            else:
                r0 = low_square
            c0 = c*low_square
            pygame.draw.rect(win, SECOND_COLOR, (c0, OFFSET + SQUARE_SIDE*8 + r0, low_square, low_square))
            pygame.draw.rect(win, SECOND_COLOR, (c0, OFFSET - low_square - r0, low_square, low_square))
            c += 1

        # Draw board grid, pointer, pieces
        for c, col in enumerate(bo.board):
            for r, cell in enumerate(col):
                c0 = c*SQUARE_SIDE
                r0 = r*SQUARE_SIDE

                # Draw board grid
                if (c % 2 == 0) ^ (r % 2 == 0):
                    pygame.draw.rect(win, SECOND_COLOR, (c0, r0 + OFFSET, SQUARE_SIDE, SQUARE_SIDE))

                # Draw pointer
                if pointer_c == c and pointer_r == r and selected is not None:
                    pygame.draw.circle(win, (186, 212, 233), (int((c + 0.5)*SQUARE_SIDE), int((r + 0.5)*SQUARE_SIDE) + OFFSET), int(SQUARE_SIDE*0.45))

                # Draw pieces
                if cell != 0:
                    if selected is None or (c, r) != selected[0]:
                        win.blit(IMAGES[cell.image], (c0, r0 + OFFSET))

        # Draw text
        if bo.ready:
            color_info = SMALL_BOLD_FONT.render('YOU ARE ' + color.upper(), True, (0, 0, 0))
            win.blit(color_info, (int(SQUARE_SIDE*4 - color_info.get_width()/2), int(OFFSET*0.5 - low_square - color_info.get_height()*0.52)))
            turn_info = SMALL_BOLD_FONT.render(bo.turn.upper() + ' TURN', True, (0, 0, 0))
            win.blit(turn_info, (int(SQUARE_SIDE*4 - turn_info.get_width()/2), int(8.85*SQUARE_SIDE - turn_info.get_height()*0.52)))
            p2Time = SMALL_FONT.render(f"{bo.p2Name}'s time: {normalize(bo.p2Time / 60)}:{normalize(bo.p2Time % 60)}", True, (0, 0, 0))
            win.blit(p2Time, (int(SQUARE_SIDE*8 - p2Time.get_width() - 5), int(OFFSET*0.5 - low_square - p2Time.get_height()*0.52)))
            p1Time = SMALL_FONT.render(f"{bo.p1Name}'s time: {normalize(bo.p1Time / 60)}:{normalize(bo.p1Time % 60)}", True, (0, 0, 0))
            win.blit(p1Time, (int(SQUARE_SIDE*8 - p1Time.get_width() - 5), int(8.85*SQUARE_SIDE - p1Time.get_height()*0.52)))
        else:
            game_info = LARGE_FONT.render('Waiting for other players...', True, (0, 0, 0))
            win.blit(game_info, (int(SQUARE_SIDE*4 - game_info.get_width()/2), int(OFFSET + SQUARE_SIDE*4 - game_info.get_height()/2)))

        # Draw selected piece
        if selected is not None:
            win.blit(IMAGES[selected[1].image], (pointer_x, pointer_y))

    # Start main game loop
    while running:

        # Request board from server
        if count == int(FPS/4):
            bo = n.send("get")
            count = 0
        else:
            count += 1

        # Check oponent's status
        if bo is None:
            print('[ERROR] Other player left')
            running = False
            end_screen(SCREEN, 'Other player left')
            break

        # Check is game over
        if bo.winner == "white":
            running = False
            end_screen(SCREEN, "White is the Winner!")
            break
        elif bo.winner == "black":
            running = False
            end_screen(SCREEN, "Black is the winner")
            break

        # Event pull
        for event in pygame.event.get():

            # Quit from app
            if event.type == pygame.QUIT:
                n.disconnect()
                running = False
                break

            # Resize window
            elif event.type == pygame.VIDEORESIZE:
                if win.get_height() != event.h:
                    resize_screen(int(event.h/9))
                elif win.get_width() != event.w:
                    resize_screen(int(event.w/8))

            # Press mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN and bo.ready:
                mous_x, mous_y = event.pos
                start_c, start_r = int(mous_x/SQUARE_SIDE), int((mous_y - OFFSET)/SQUARE_SIDE)
                if mous_y >= OFFSET and start_r <= 7:
                    piece = bo.board[start_c][start_r]
                    if piece != 0 and color == bo.turn and piece.color == color:
                        bo = n.send('update moves')
                        dragging = True
                        selected = ((start_c, start_r), piece)
                        start_x, start_y = start_c*SQUARE_SIDE, start_r*SQUARE_SIDE + OFFSET
                        pointer_x, pointer_y = start_x, start_y
                        offset_x, offset_y = mous_x - start_x, mous_y - start_y

            # Mouse motion
            elif event.type == pygame.MOUSEMOTION and dragging:
                mous_x, mous_y = event.pos
                pointer_x, pointer_y = mous_x - offset_x, mous_y - offset_y

            # Release mouse button
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging and piece.color == bo.turn and color == bo.turn:
                    mous_x, mous_y = event.pos
                    finish_c = int((mous_x - offset_x)/SQUARE_SIDE + 0.5)
                    finish_r = int((mous_y - offset_y - OFFSET)/SQUARE_SIDE + 0.5)
                    if bo.must_atack:
                        bo = n.send(f"atack {start_c} {start_r} {finish_c} {finish_r}")
                    else:
                        bo = n.send(f"move {start_c} {start_r} {finish_c} {finish_r}")

                dragging = False
                selected = None

        refresh_board()
        pygame.display.update()
        clock.tick(FPS)


def resize_screen(square_side_len):
    global SCREEN
    global SQUARE_SIDE, OFFSET
    global images, IMAGES
    global LARGE_FONT, SMALL_BOLD_FONT, SMALL_FONT
    SQUARE_SIDE = square_side_len
    SCREEN = pygame.display.set_mode((SQUARE_SIDE*8, SQUARE_SIDE*9), pygame.RESIZABLE)
    OFFSET = int(SQUARE_SIDE/2)
    LARGE_FONT = pygame.font.Font(resource_path('fonts\\Segoe UI Italic.ttf'), int(SQUARE_SIDE*0.65))
    SMALL_FONT = pygame.font.Font(resource_path('fonts\\Segoe UI Italic.ttf'), int(SQUARE_SIDE*0.3))
    SMALL_BOLD_FONT = pygame.font.Font(resource_path('fonts\\Segoe UI Bold Italic.ttf'), int(SQUARE_SIDE*0.3), bold=True)
    IMAGES = [pygame.transform.scale(image, (SQUARE_SIDE, SQUARE_SIDE)) for image in images]


def connect():
    global n
    n = Network()
    return n


def end_screen(win, text):
    pygame.font.init()
    txt = LARGE_FONT.render(text, 1, (0, 0, 0))
    win.fill(FIRST_COLOR)
    win.blit(txt, (int(SQUARE_SIDE*4 - txt.get_width()/2), int(SQUARE_SIDE*4 - txt.get_height()/2 + OFFSET)))
    pygame.display.update()

    pygame.time.set_timer(pygame.USEREVENT+1, 3000)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                n.disconnect()
                pygame.quit()
                quit()
                running = False
            elif event.type == pygame.KEYDOWN:
                running = False
            elif event.type == pygame.USEREVENT+1:
                running = False


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

images = [
    pygame.image.load(resource_path('images\\men_white.png')),
    pygame.image.load(resource_path('images\\king_white.png')),
    pygame.image.load(resource_path('images\\men_black.png')),
    pygame.image.load(resource_path('images\\king_black.png'))
    ]

#TODO menu name require
name = input('Enter your name:')

SQUARE_SIDE = 80
OFFSET = int(SQUARE_SIDE/2)
FPS = 60
FIRST_COLOR = (255, 255, 255)     # White
SECOND_COLOR = (140, 184, 219)    # Blue light
SCREEN = pygame.display.set_mode((SQUARE_SIDE*8, SQUARE_SIDE*9), pygame.RESIZABLE)
LARGE_FONT = pygame.font.Font(resource_path('fonts\\Segoe UI Italic.ttf'), 52)
SMALL_FONT = pygame.font.Font(resource_path('fonts\\Segoe UI Italic.ttf'), 24)
SMALL_BOLD_FONT = pygame.font.Font(resource_path('fonts\\Segoe UI Bold Italic.ttf'), 24)
IMAGES = [pygame.transform.scale(image, (SQUARE_SIDE, SQUARE_SIDE)) for image in images]

pygame.display.set_icon(pygame.image.load(resource_path('images\\icon.png')))
pygame.display.set_caption('Checkers')
clock = pygame.time.Clock()

try:
    bo = connect()
    main(SCREEN)
except Exception as e:
    print('[ERROR] ' + str(e))
    print('Server Offline')


pygame.quit()
