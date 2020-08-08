class Chessman:
    def __init__(self,pos,state,image):
        self.pos = pos
        self.state = state
        self.image = image
    def kill(self):
        self.state = False
    def availablePos(self):
        pass
    def isReachable(self,pos):
        pass
    def moveTo(self,pos):
        pass

class Knight(Chessman):
    def __init__(self,pos,state,image):
        super().__init__(pos,state,image)
    def availablePos(self):
        return [1,2,3]
    def isReachable(self,pos):
        return(pos[0] == 1 and pos[1] == 2)
    def moveTo(self,pos):
        #Implementar validacion
        self.pos = pos

if(__name__ == '__main__'):
    #Ejemplo medio chafa de como funciona esto
    testK = Knight((0,0),False,"Image")
    print(testK.isReachable((1,2)))
    testK.moveTo((8,8))
    print(testK.pos)
