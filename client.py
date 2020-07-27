import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.100.10"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
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

trn = read_msg(client)
ter = True

if(trn == b'!T1'): ter = True
else: ter = False

print(trn, ter)

while True:

    if(ter):
        msg = input()
        send(msg)
        ter = not ter
    else: 
        rec = read_msg(client)
        print(rec)
        ter = not ter
        if(rec == "!GG"): break