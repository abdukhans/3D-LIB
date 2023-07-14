from graphics import *
from Vec2D import Vec2D
class Tris2D:
    def __init__(self,p1:Vec2D,p2:Vec2D, p3:Vec2D):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        p_p1   = Point(self.p1.x,self.p1.y)
        p_p2   = Point(self.p2.x,self.p2.y)
        p_p3   = Point(self.p3.x,self.p3.y)
        self.poly = Polygon(p_p1,p_p2,p_p3,p_p1)



    def setFill(self,color): 
        self.poly.setFill(color)

    def setOutline(self,color):
        self.poly.setOutline(color)
    def draw_tri (self, win:GraphWin):  
        

        # for i in range(300):
        #     for j in range(300):
        #         win.plotPixel(100 + i,100 + j ,color="red")

        self.poly.draw(win)

        pass
