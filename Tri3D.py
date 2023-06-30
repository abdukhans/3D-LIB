from Vec3D import Vec3D

class Tris3D:
    def __init__(self, p1:Vec3D,p2:Vec3D, p3:Vec3D,col="white"):
        self.p1 = p1
        self.p2 = p2 
        self.p3 = p3
        
        
        self.norm = (self.p1 - self.p2).crossProd(self.p2 - self.p3).normalizeVec()
        self.col  = col

       
    def getPoints(self) :
        return [self.p1,self.p2,self.p3]

    def setCol (self, color):
        self.col = color

    """
    def drawTri(self,window: GraphWin):
        self.l1.draw(window)
        self.l2.draw(window)
        self.l3.draw(window)
    """
    def midPoi(self):

        return 1/3*(self.p1 + self.p2 + self.p3)
        
    def rotateZ_(self,ang):

        self.p1.rotateZ_(ang)
        self.p2.rotateZ_(ang)
        self.p3.rotateZ_(ang)

        #self.norm = (self.p1 - self.p2).crossProd(self.p2 - self.p3).normalizeVec()

        return
    def rotateY_ (self,ang):
        self.p1.rotateY_(ang)
        self.p2.rotateY_(ang)
        self.p3.rotateY_(ang)

        #self.norm = self.p1.crossProd(self.p2).normalizeVec()

        return

    def rotateX_(self,ang):
        self.p1.rotateX_(ang)
        self.p2.rotateX_(ang)
        self.p3.rotateX_(ang)


        #self.norm = self.p1.crossProd(self.p2).normalizeVec()

        return

    def updateNorm(self):
        self.norm = (self.p1 - self.p2).crossProd(self.p2 - self.p3).normalizeVec()

    def scale(self,factor):

        self.p1 = factor*self.p1
        self.p3 = factor*self.p2
        self.p3 = factor*self.p3
        self.norm = factor*self.norm

    def move(self, trans_vec):

        self.p1.transVec(trans_vec)
        self.p2.transVec(trans_vec)
        self.p3.transVec(trans_vec)

    def __str__(self):

        return (str(self.p1) +"\n" + str(self.p2) + "\n" + str(self.p3))