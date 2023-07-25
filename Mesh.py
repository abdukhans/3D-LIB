import numpy as np
from Vec3D import Vec3D
from Tri3D import Tris3D

class Mesh:
    def __init__(self, lst3d_tris:list[Tris3D],file_path="",use_numpy=False):
        self.lst3d_tris = lst3d_tris
        self.lst_vs:set = set()
        self.numpListTri = np.zeros(shape=(0,3,3),dtype=np.float64)
        for i in self.lst3d_tris:
            """if i.p1 not in self.lst3d_tris:
                self.lst_vs.add(i.p1)
            if i.p2 not in self.lst3d_tris:
                self.lst_vs.add(i.p2)
            if i.p3 not in self.lst3d_tris:
                self.lst_vs.add(i.p3)"""

            self.lst_vs.add(i.p1)
            self.lst_vs.add(i.p2)
            self.lst_vs.add(i.p3)
        """for i in (self.lst_vs):
            print(i)"""
        
        if file_path != "" and not(use_numpy):
            self.file = file_path
            self.createObj()
            self.lst_vs:set = set()
            for i in self.lst3d_tris:
                """if i.p1 not in self.lst3d_tris:
                    self.lst_vs.add(i.p1)
                if i.p2 not in self.lst3d_tris:
                    self.lst_vs.add(i.p2)
                if i.p3 not in self.lst3d_tris:
                    self.lst_vs.add(i.p3)"""

                self.lst_vs.add(i.p1)
                self.lst_vs.add(i.p2)
                self.lst_vs.add(i.p3)
        elif file_path!="":
            self.file =  file_path
            self.createNumpObj()

            self.lst_vs:set = set()
            for i in self.lst3d_tris:
                """if i.p1 not in self.lst3d_tris:
                    self.lst_vs.add(i.p1)
                if i.p2 not in self.lst3d_tris:
                    self.lst_vs.add(i.p2)
                if i.p3 not in self.lst3d_tris:
                    self.lst_vs.add(i.p3)"""

                self.lst_vs.add(i.p1)
                self.lst_vs.add(i.p2)
                self.lst_vs.add(i.p3)




            pass
        
        
        self.isNumpy = use_numpy



        #print(len(self.lst_vs))
    def createObj(self):
        lst_verts = []
        num_nums_added = 0 
        with open(self.file) as file:
            string = file.read()

            lst_format = string.split('\n')
            #lst_string  = "".join(lst_format).split(" ")
            num_vert_read = 0 
            floats = []
            idx = 0 
            #print(lst_format)
            while idx < len (lst_format):

                str_elm = lst_format[idx]
                
                str_elm_f = str_elm.split(" ")
                #print(str_elm_f)

                if str_elm_f[0] == "v":
                    lst_verts.append(Vec3D( float(str_elm_f[1] ), float(str_elm_f[2]) , float(str_elm_f[3])))
                
                idx += 1

            #print(len(lst_verts))
            idx = 0 
            # global parse_3d_tris
            # global numpy_num_tris_3BC
            # numpy_num_tris_3BC = 0
                    
            while idx < len (lst_format):
                str_elm = lst_format[idx]
                
                str_elm_f = str_elm.split(" ")
                #print(str_elm_f)
                if str_elm_f[0] == "f":
                    id1 = int(str_elm_f[1])
                    id2 = int (str_elm_f[2])
                    id3 = int(str_elm_f[3])


                    if idx %1 == 0:
                        self.lst3d_tris.append(Tris3D(lst_verts[id1 - 1],lst_verts[id2 - 1],lst_verts[id3 - 1]))


                        # if parse_3d_tris:
                        #     # if numpy_num_tris_3BC == 0 :
                        #     #     print(self.lst3d_tris[numpy_num_tris_3BC])
                        #     for point in range(3):
                        #         for cord in range(3):

                        #             text_cord = self.lst3d_tris[numpy_num_tris_3BC].getPoints()[point].numpify()[cord]
                        #             list_3d_numpy_BC[9*numpy_num_tris_3BC + 3*point + cord ] = text_cord

                        #             #print(9*numpy_num_tris_3BC + 3*point + cord )
                        #             num_nums_added += 1
                            
                        #     numpy_num_tris_3BC += 1 
                idx  += 1


            #print("OBJ CREATION: " , self.lst3d_tris[0], "\n------------")
            #print(list_3d_numpy_BC)
            #print("LEN: ", len(self.lst3d_tris))
        print(self.lst3d_tris[0])
        # if parse_3d_tris:
        #     print("num_nums_added         : ", num_nums_added) 
        #     print("len of list_3d_numpy_BC: ", len(list_3d_numpy_BC)) 
        #     print("numpy_num_tris_3BC     : ", numpy_num_tris_3BC)
        #     print("NUM 3d TRIS            : ", len(self.lst3d_tris))
        
        #     #print("numpy_num_tris_3BC: ", numpy_num_tris_3BC)
        #     with open('BC_3D.txt', 'w+') as fp:
        #         fp.write("\n".join(str(item) for (idx, item) in enumerate(list_3d_numpy_BC) if idx < 9*numpy_num_tris_3BC ))

            

                

            


        
        pass

    def createNumpObj(self):
        lst_verts = []
        with open(self.file) as file:
            string = file.read()
            lst_format = string.split('\n')
            #lst_string  = "".join(lst_format).split(" ")
            num_vert_read = 0 
            floats = []
            idx = 0 
            #print(lst_format)
            while idx < len (lst_format):

                str_elm = lst_format[idx]
                
                str_elm_f = str_elm.split(" ")
                #print(str_elm_f)

                if str_elm_f[0] == "v":
                    lst_verts.append(Vec3D( float(str_elm_f[1] ), float(str_elm_f[2]) , float(str_elm_f[3])))
                
                idx += 1

            #print(len(lst_verts))
            idx = 0 
            # global parse_3d_tris
            # global numpy_num_tris_3BC
            # numpy_num_tris_3BC = 0
                    
            while idx < len (lst_format):
                str_elm = lst_format[idx]                
                str_elm_f = str_elm.split(" ")
                #print(str_elm_f)
                if str_elm_f[0] == "f":
                    id1 = int(str_elm_f[1])
                    id2 = int (str_elm_f[2])
                    id3 = int(str_elm_f[3])
                    if idx %1 == 0:
                        v1 = lst_verts[id1 - 1]
                        v2 = lst_verts[id2 - 1]
                        v3 = lst_verts[id3 - 1]
                        numpTri = np.array([[[v1.x,v1.y,v1.z],
                                             [v2.x,v2.y,v2.z],
                                             [v3.x,v3.y,v3.z]]],dtype=np.float64)
                        self.numpListTri = np.append(self.numpListTri,numpTri,axis=0)
                        self.lst3d_tris.append(Tris3D(lst_verts[id1 - 1],lst_verts[id2 - 1],lst_verts[id3 - 1]))
                idx  += 1


        print("NUMP TRIS[0]: ",self.numpListTri[0], "LIST TRIS[0]: ",self.lst3d_tris[0])


        







        pass




    def createNumpObjFromVerts(self):

        self.isNumpy = True
        tri_idx = 0 
        self.numpListTri = np.zeros(shape=(len(self.lst3d_tris),3,3),dtype=np.float64)
        for tri in self.lst3d_tris: 
            point_idx =0 
            for vec in tri.getPoints():
                cord_idx = 0 
                for cord in vec.numpify():

                    self.numpListTri[tri_idx][point_idx][cord_idx] = cord
                    cord_idx += 1 

                    

                        


                    pass
                
                point_idx += 1
            pass

            tri_idx +=1 

        pass
    def move(self,trans_vec:Vec3D):
        for i in self.lst_vs:
            i.transVec(trans_vec)



    def rotateX_(self,degrees):
        for i in self.lst_vs:
            i.rotateX_(degrees)
        self.updateNorms()



    def rotateY_(self,degrees):
        for i in self.lst_vs:
            i.rotateY_(degrees)
        self.updateNorms()


    def rotateZ_(self,degrees):
        for i in self.lst_vs:
            i.rotateZ_(degrees)
        self.updateNorms()


    def updateNorms(self):
        for tris in self.lst3d_tris:
            tris.updateNorm()

    def scale (self, factor):
        new_lst = set()
        for v in self.lst_vs:
            nv:Vec3D = v*(factor)
            v.set_coords(nv.x,nv.y,nv.z)

    def __mul__(self,factor):
        new_mesh = Mesh (self.lst3d_tris)
        return new_mesh.scale(factor)

    def __rmul__(self,factor):
        return self.__mul__(factor)