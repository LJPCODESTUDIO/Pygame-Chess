import socket
import pickle
from _thread import *
from game import Game

server = "127.0.0.1"
port = 5555
connected = set()
games = {}
id_count = 0
HEADERSIZE  = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))


s.listen()
print("Sever started")
print("Waiting for connections")

# Credit: Simon vW(StackOverflow) I believe I mostly understand what they did here
def receive_data(sock):
    full_msg = b''
    new_msg = True
    while True:
        msg = sock.recv(16)
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg

        if len(full_msg)-HEADERSIZE == msglen:
            data = pickle.loads(full_msg[HEADERSIZE:])
            break

    return data


def send_data(clientsocket, data):
    data_to_send = pickle.dumps(data)
    data_size = bytes(f'{len(data_to_send):<{10}}', "utf-8")
    try:
        clientsocket.send(data_size + data_to_send)
        
    except socket.error as e:
        print(e)


def threadedClient(conn, p, game_id):
    global id_count 
    conn.send(str.encode(str(p)))
    
    reply = ""
    while True:
        try:
            data = receive_data(conn)
            # check if the game still exists
            if game_id in games:
                game = games[game_id]
                
                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset()
                    elif data != "get":
                        game.play(p, data)
                        
                    reply = game
                    
                    send_data(conn, reply)

            else:
                break
        except Exception as e:
            print("Failed try")
            print(e)
            break
        
    print("Lost connection")
    
    try:
        print("Closing game", game_id)
        del games[game_id]
    except:
        pass
    
    id_count -=1
    conn.close()


while True:
    conn, addr = s.accept()
    print(f"Connected to: {addr}")

    id_count += 1
    p = 0
    game_id = (id_count - 1)//2
    if id_count % 2 == 1:
        games[game_id] = Game(game_id)
        print("Creating a new game...")
    else:
        games[game_id].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, game_id))