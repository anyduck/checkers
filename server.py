import socket
from _thread import *
from board import Board
import pickle
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "0.0.0.0"
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print('[ERROR SOCKET] ', e)

s.listen()
print("[START] Waiting for a connection")

connections = 0

games = {0: Board(8, 8)}


def threaded_client(conn, game):
    global games, connections

    name = None
    bo = games[game]

    if connections % 2 == 0:
        currentId = "white"
    else:
        bo.ready = True
        bo.start_time = time.time()
        currentId = "black"

    bo.start_user = currentId

    # Pickle the object and send it to the server
    data_string = pickle.dumps(bo)

    conn.send(data_string)
    connections += 1

    while True:
        if game not in games:
            break

        try:
            d = conn.recv(8192 * 3)
            data = d.decode("utf-8")
            if not d:
                break
            else:

                if bo.p1Time < 0:
                    bo.winner = "black"
                    print("[GAME] Player" + bo.p2Name + "won in game", game)
                if bo.p2Time < 0:
                    bo.winner = "white"
                    print("[GAME] Player" + bo.p1Name + "won in game", game)

                # if data == "update moves":
                #     bo.update_moves()

                if "atack " in data:
                    move_list = data.split()
                    bo.make_atack(int(move_list[1]), int(move_list[2]), int(move_list[3]), int(move_list[4]))
                elif "move " in data:
                    move_list = data.split()
                    bo.make_move(int(move_list[1]), int(move_list[2]), int(move_list[3]), int(move_list[4]))
                elif "name " in data:
                    name = data[5:]
                    if currentId == "black":
                        bo.p2Name = name
                    elif currentId == "white":
                        bo.p1Name = name

                if bo.ready:
                    if bo.turn == "white":
                        bo.p1Time = bo.p1PrevTime - time.time() + bo.start_time
                    else:
                        bo.p2Time = bo.p2PrevTime - time.time() + bo.start_time

                sendData = pickle.dumps(bo)

            conn.sendall(sendData)

        except Exception as e:
            print(f'[ERROR GAME {game}] ', e)
            break

    connections -= 1
    try:
        del games[game]
        print("[GAME] Game", game, "ended")
    except:
        pass
    print("[DISCONNECT] Player", name, "left game", game)
    conn.close()


while True:
    if connections < 11:
        conn, addr = s.accept()
        g = -1
        print("[CONNECT] New connection")

        for game in games.keys():
            if games[game].ready is False:
                g = game

        if g == -1:
            try:
                g = list(games.keys())[-1]+1
                games[g] = Board(8, 8)
            except:
                g = 0
                games[g] = Board(8, 8)

        print("[DATA] Number of Connections:", connections+1)
        print("[DATA] Number of Games:", len(games))

        start_new_thread(threaded_client, (conn, g))
