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

def send(msg, client):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

def read_msg(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length)
        return msg
        
def create_lobby(conn1, addr1, conn2, addr2):
    print(f"[NEW LOBBY] {addr1} : {addr2}")

    send("!T1", conn1)
    send("!T2", conn2)

    turno = True
    game = True
    
    while game:
        if(turno):
            msg = read_msg(conn1)
            if(msg == "!LOSE"):
                print("Gana el 2")
                game = False
                send("!GG", conn1)
                send("!GG", conn2)
            else:
                send(msg, conn2)
            
        else:
            msg = read_msg(conn2)
            if(msg == "!LOSE"):
                print("Gana el 1")
                game = False
                send("!GG", conn1)
                send("!GG", conn2)
            else:
                send(msg, conn1)

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