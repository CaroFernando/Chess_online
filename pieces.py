class Chessman:
    def __init__(self,pos,color,image):
        self.pos = pos
        self.color = color 
        self.image = image
    def moveTo(self,pos):
        self.pos = pos

    def availablePos(self,board):
        pass

    @staticmethod
    def isValid(initialPos, targetPos):
        return initialPos != targetPos and 0 <= targetPos[0] <= 7 and 0 <= targetPos[1] <= 7

    @staticmethod
    def linearMovement(a,b,isBlocked,piece,moves,j,board):
        if isValid(piece.pos, (x := piece.pos[0] + a, y := piece.pos[1] + b)) and not isBlocked[j]:
            if board[y][x] != piece.color: moves.append((x, y))
            if board[y][x] != 0: isBlocked[j] = True

    
class Queen(Chessman):
    def __init__(self,pos,state,image):
        super().__init__(pos,state,image)

    def availablePos(self,board):
        moves = []
        aBlocked, tBlocked = [False] * 4, [False] * 4
        for i in range(8):
            for j in range(4):
                Chessman.linearMovement(-i if j < 2 else i, i if j % 2 else -i, aBlocked, self, moves, j, board)
                Chessman.linearMovement(0 if j < 2 else i if not j % 2 else -i, 0 if j > 1 else i if not j % 2 else -i, tBlocked, self, moves, j,board)
        return moves

class Bishop(Chessman):
    def __init__(self,pos,state,image):
        super().__init__(pos,state,image)

    def availablePos(self,board):
        moves = []
        isBlocked = [False] * 4
        for i in range(8):
            for j in range(4):
                Chessman.linearMovement(-i if j < 2 else i, i if j % 2 else -i, isBlocked, self, moves, j,board)
        return moves
    
class Knight(Chessman):
    def __init__(self,pos,state,image):
        super().__init__(pos,state,image)

    def availablePos(self,board):
        moves = []
        for i in range(4):
            for j in range(2):
                x, y = self.pos[0] + (1 if i % 2 else -1) * (2 if not j % 2 else 1), self.pos[1] + (1 if i < 2 else -1) * (2 if j % 2 else 1)
                if Chessman.isValid(self.pos, (x, y)) and board[y][x] != piece.color: moves.append((x, y))
        return moves

if(__name__ == '__main__'):
    #Ejemplo medio chafa de como funciona esto
    print(Chessman.isValid((0,0),(0,0)))
