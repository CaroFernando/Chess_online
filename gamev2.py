"""
Es básicamente lo mismo, pero un poco mas claro
Solo se implementan las clases cuando hay que checar las posiciones desponibles
Es debatible que este sea un mejor approach que el planteado originalemente, aunque
considero que hacerlo de esta forma hace que el código sea más claro y mantenible
"""

import pygame, os, sys, json
from pieces import *

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
    "db":[(3,7)],
    "dn":[(3,0)],
    "ab":[(2,7),(5,7)],
    "an":[(2,0),(5,0)],
    "cb":[(1,7),(6,7)],
    "cn":[(1,0),(6,0)],
    "tb":[(0,7),(7,7)],
    "tn":[(0,0),(7,0)]
}

# movimiento de piezas ----------------------
dragdrop = True
passant = pieza_mov = None
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
                            if turn == i[1]:
                                obj = None
                                if(i[0]=='d'):obj = Queen(state[i][j],i[1])
                                if(i[0]=='a'):obj = Bishop(state[i][j],i[1])
                                if(i[0]=='c'):obj = Knight(state[i][j],i[1])
                                if(i[0]=='t'):obj = Rook(state[i][j],i[1])
                                mov = obj.availablePos(board)
                                print(mov)
                                if len(mov): 
                                    dragdrop = False
            else:                                
                if (tabx, taby) in mov:
                    coor = state[pieza_mov[0]][pieza_mov[1]]           
                    passant = coor[0] if pieza_mov[0][0] == "p" and abs(coor[1] - taby) == 2 else None
                    turn = "n" if pieza_mov[0][1] == "b" else "b"
                    board[taby][tabx], board[coor[1]][coor[0]] = board[coor[1]][coor[0]], 0
                    state[pieza_mov[0]][pieza_mov[1]] = (tabx, taby)
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


