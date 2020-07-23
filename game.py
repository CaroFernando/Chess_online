import pygame
import os
import sys
import json

pygame.init()
win = pygame.display.set_mode((1000, 800))

pygame.display.set_caption("ajedrez")

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
                            dragdrop = False
            else:
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

    pygame.display.update()

pygame.quit()

