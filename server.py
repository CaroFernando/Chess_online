import socket 
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()

def read_msg(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length)
        return msg
        
def create_lobby(conn1, addr1, conn2, addr2):
    print("Gemu stato")

    turno = True
    game = True
    while game:
        if(turno):
            msg = read_msg(conn1)
            if(msg == "!LOSE"):
                print("Gana el 2")
                game = False
                conn1.send("!GG".enconde(FORMAT))
                conn2.send("!GG".enconde(FORMAT))
            else:
                conn2.send(msg)
            
        else:
            msg = read_msg(conn2)
            if(msg == "!LOSE"):
                print("Gana el 1")
                game = False
                conn1.send("!GG".enconde(FORMAT))
                conn2.send("!GG".enconde(FORMAT))
            else:
                conn1.send(msg)

        turno = not turno

    conn1.close()
    conn2.close()

    print("Fin del juego")

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn1, addr1 = server.accept()
        conn2, addr2 = server.accept()

        print("[CREATE LOBBY]")
        thread = threading.Thread(target=create_lobby, args=(conn1, addr1, conn2, addr2))
        thread.start()



print("[STARTING] server is starting...")
start()