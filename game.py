import pygame
import os
import sys
import json
def isValid(piece, x):
    return x != piece[1] and 0 <= x[0] <= 7 and 0 <= x[1] <= 7
def linearMovement(a, b, isBlocked, piece, moves, j):
    if isValid(piece, (x := piece[1][0] + a, y := piece[1][1] + b)) and not isBlocked[j]:
        if board[y][x] != piece[0][1]: moves.append((x, y))
        if board[y][x] != 0: isBlocked[j] = True
def PossibleMovements(piece):
    moves = []
    if(piece[0][0] == "r"):
        for i in range(piece[1][0]-1, piece[1][0]+2):       
            for j in range(piece[1][1]-1, piece[1][1]+2):
                if isValid(piece, (i,j)) and board[j][i] != piece[0][1]: moves.append((i, j))
    elif(piece[0][0] == "d"):
        aBlocked, tBlocked = [False] * 4, [False] * 4
        for i in range(8):
            for j in range(4):
                linearMovement(-i if j < 2 else i, i if j % 2 else -i, aBlocked, piece, moves, j)
                linearMovement(0 if j < 2 else i if not j % 2 else -i, 0 if j > 1 else i if not j % 2 else -i, tBlocked, piece, moves, j)
    elif(piece[0][0] == "t"):
        isBlocked = [False] * 4
        for i in range(8):
            for j in range(4):
                linearMovement(0 if j < 2 else i if not j % 2 else -i, 0 if j > 1 else i if not j % 2 else -i, isBlocked, piece, moves, j)
    elif(piece[0][0] == "a"):     
        isBlocked = [False] * 4
        for i in range(8):
            for j in range(4):
                linearMovement(-i if j < 2 else i, i if j % 2 else -i, isBlocked, piece, moves, j) 
    elif(piece[0][0] == "c"):
        for i in range(4):
            for j in range(2):
                x, y = piece[1][0] + (1 if i % 2 else -1) * (2 if not j % 2 else 1), piece[1][1] + (1 if i < 2 else -1) * (2 if j % 2 else 1)
                if isValid(piece, (x, y)) and board[y][x] != piece[0][1]: moves.append((x, y))
    elif(piece[0][0] == "p"):   
        for i in range(3):
            if isValid(piece, (x := (piece[1][0] + i - 1), y := piece[1][1] + (1 if piece[0][1] == "n" else -1))) and board[y][x] == (0 if i == 1 else "b" if piece[0][1] == "n" else "n"):
                moves.append((x, y))
        if (piece[1][1] == 1 and piece[0][1] == "n") or (piece[1][1] == 6):
            if board[piece[1][1] + (2 if piece[0][1] == "n" else -2)][piece[1][0]] == 0:
                moves.append((piece[1][0], (piece[1][1] + (2 if piece[0][1] == "n" else -2))))
    return moves
        
pygame.init()
win = pygame.display.set_mode((1000, 800))

pygame.display.set_caption("Ajedrez")

tam = 70
tab_x_off = 100
tab_y_off = 80

imgpath = os.getcwd() + r'\img'

names = {"rb", "rn", "db", "dn", "ab", "an", "cb", "cn", "tb", "tn", "pb", "pn"}

images = {}

for name in names:
    images[name] = pygame.image.load(imgpath + "\\" + name + ".png")
    images[name] = pygame.transform.scale(images[name], (tam, tam))

state = {
    "rb":[(4, 7)], 
    "rn":[(4, 0)],
    "db":[(3, 7)],
    "dn":[(3, 0)],
    "ab":[(2, 7), (5, 7)],
    "an":[(2, 0), (5, 0)],
    "cb":[(1, 7), (6, 7)],
    "cn":[(1, 0), (6, 0)],
    "tb":[(0, 7), (7, 7)],
    "tn":[(0, 0), (7, 0)]
}

state["pb"] = []

for i in range(0, 8):
    state["pb"].append((i, 6))

state["pn"] = []

for i in range(0, 8):
    state["pn"].append((i, 1))

# movimiento de piezas ----------------------
dragdrop = True
pieza_mov = None
board = [[0]*8 for i in range(8)]
for i in range(2):
    for j in range(8):
        board[0+i][j] = 'n'
        board[6+i][j] = 'b'
turn = "b"
# -------------------------------------------

run = True

while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            tabx = int((pos[0] - tab_x_off)/tam)
            taby = int((pos[1] - tab_y_off)/tam)

            print(tabx, taby)

            if(dragdrop):
                for i in state:
                    for j in range(0, len(state[i])):
                        if(state[i][j][0] == tabx and state[i][j][1] == taby): 
                            print(i)
                            pieza_mov = (i, j)
                            print(turn, i[0])
                            if turn == i[1]:
                                mov = PossibleMovements((i, state[i][j]))
                                if len(mov): dragdrop = False
            else:                                
                if (tabx, taby) in mov:
                    coor = state[pieza_mov[0]][pieza_mov[1]]
                    board[taby][tabx] = board[coor[1]][coor[0]]
                    board[coor[1]][coor[0]] = 0                    
                    state[pieza_mov[0]][pieza_mov[1]] = (tabx, taby)
                    turn = "n" if pieza_mov[0][1] == "b" else "b"
                dragdrop = True

                sendmsg = json.dumps(state)
                print(sendmsg)

    for i in range(0, 8):
        for j in range(0, 8):
            if (i+j) % 2 != 0: pygame.draw.rect(win, (70, 130, 180), (tam*i + tab_x_off, tam*j + tab_y_off, tam, tam));
            else: pygame.draw.rect(win, (255, 255, 255), (tam*i + tab_x_off, tam*j + tab_y_off, tam, tam));
    for i in state: 
        for j in range(0, len(state[i])):
            win.blit(images[i], (state[i][j][0]*tam + tab_x_off, state[i][j][1]*tam + tab_y_off)) 
    if not dragdrop:
        for i in mov:
            pygame.draw.circle(win, (200, 0, 0), (tam*i[0] + tam//2 + tab_x_off, tam*i[1] + tam//2 + tab_y_off), tam//8);
    pygame.display.update()

pygame.quit()


