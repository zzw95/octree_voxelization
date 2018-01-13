import numpy as np
from stl import mesh
from collections import deque

def getBoxTriangles(triangles, box):
    intersectTriangles = []
    coincideTriangles = []
    bounds = 0
    isFill = False
    for triangle in triangles:
        state = checkIntersect(triangle, box)
        if state==1:
            # 判断重合三角形的法向
            if checkNormal(triangle, box):
                coincideTriangles.append(triangle)
        elif state==2:
            intersectTriangles.append(triangle)
        else:
            if checkBound(triangle, box):
                bounds+=1
    if bounds==len(triangles):
        isFill = True
    return coincideTriangles, intersectTriangles, isFill

def checkIntersect(triangle, box):
    """
    :param triangle: array, shape=(4,3)
    :param box: list,len=6
    :return: 0 -> not intersect
            1 -> cocincide
            2 -> intersect
    """
    isOn = False
    if (triangle[:3,0]==box[0]).all():
        isOn = True
    elif (triangle[:3,0]<=box[0]).all():
        return 0

    if (triangle[:3,0]==box[3]).all():
        isOn = True
    elif (triangle[:3,0]>=box[3]).all():
        return 0

    if (triangle[:3,1]==box[1]).all():
        isOn = True
    elif (triangle[:3,1]<=box[1]).all():
        return 0

    if (triangle[:3,1]==box[4]).all():
        isOn = True
    elif (triangle[:3,1]>=box[4]).all():
        return 0

    if (triangle[:3,2]==box[2]).all():
        isOn = True
    elif (triangle[:3,2]<=box[2]).all():
        return 0

    if (triangle[:3,2]==box[5]).all():
        isOn = True
    elif (triangle[:3,2]>=box[5]).all():
        return 0

    if isOn:
        return 1
    else:
        return 2


def checkNormal(ctriangle, box):
    """
    :param ctriangle: array, shape=(4,3)
    :param box: list,len=6
    :return: False -> normal oppsite
            True -> normal same
    """
    if (ctriangle[:3,0]==box[0]).all():
        return True if ctriangle[3,0]<0 else False
    elif (ctriangle[:3,0]==box[3]).all():
        return True if ctriangle[3,0]>0 else False

    elif (ctriangle[:3,1]==box[1]).all():
        return True if ctriangle[3,1]<0 else False
    elif (ctriangle[:3,1]==box[4]).all():
        return True if ctriangle[3,1]>0 else False

    elif (ctriangle[:3,2]==box[2]).all():
        return True if ctriangle[3,2]<0 else False
    elif (ctriangle[:3,2]==box[5]).all():
        return True if ctriangle[3,2]>0 else False

    else:
        raise ValueError

def checkBound(triangle, box):
    # 如果三角形的外法向与体素盒到三角形重心的矢量方向相同，则体素盒被三角形包围，return True
    c1 = np.array([np.mean(triangle[:3,0]), np.mean(triangle[:3,1]), np.mean(triangle[:3,2])])
    c2 = np.array([(box[0]+box[3])/2, (box[1]+box[4])/2, (box[2]+box[5])/2])
    if(np.dot(triangle[3],c1-c2)>0):
        return True
    else:
        return False

def calVolumeFraction(itriangle, box):
    return 1
    '''
    1. 三角形一定完全穿过体素盒
    2. 已知平面上一点(x0,y0,z0)和法向量(A,B,C), 则平面的点法式方程为A(x-x0)+B(y-y0)+C(z-z0)=0
    3. 求体素盒的12条边与三角形的交点
    '''
    # cross=[]
    # A, B, C = itriangle[3]
    # x0, y0, z0 = itriangle[0]
    #
    # if A!=0:
    #     y = np.array([box[1], box[1], box[4], box[4]])
    #     z = np.array([box[2], box[5], box[2], box[5]])
    #     x = -(B*(y-y0) + C*(z-z0)) / A + x0
    #     for i in range(4):
    #         if x[i]>= box[0] and x[i]<= box[3]:
    #             cross.append([x[i], y[i], z[i]])
    #
    # if B!=0:
    #     x = np.array([box[0], box[0], box[3], box[3]])
    #     z = np.array([box[2], box[5], box[2], box[5]])
    #     y = -(A*(x-x0) + C*(z-z0)) / B + y0
    #     for i in range(4):
    #         if y[i]>= box[1] and y[i]<= box[4]:
    #             cross.append([x[i], y[i], z[i]])
    #
    # if C!=0:
    #     x = np.array([box[0], box[0], box[3], box[3]])
    #     y = np.array([box[1], box[1], box[4], box[4]])
    #     z = -(A*(x-x0) + B*(y-y0)) / C + z0
    #     for i in range(4):
    #         if z[i]>= box[2] and z[i]<= box[5]:
    #             cross.append([x[i], y[i], z[i]])
    #
    # # Normalization
    # cross = np.array(cross)
    # cross = (cross-np.array([box[0], box[1], box[2]])) / np.array(box[3]-box[0], box[4]-box[1], box[5]-box[2])
    #
    # # 计算体积太过复杂， 解决方案是计算体素盒中心到三角形的距离，除以包围盒的对角线， 并正则化到区间[0,1]
    # box_c = np.array([(box[0]+box[3])/2, (box[1]+box[4])/2, (box[2]+box[5])/2])
    # section_c = np.array([np.mean(cross[:,0]), np.mean(cross[:,1]), np.mean(cross[:,2])])
    # dist = np.linalg.norm(section_c - box_c)
    # most = True if np.dot(itriangle[3],section_c - box_c)>0 else False
    #
    # if len(cross)==3:
    #     l = np.linalg.norm(box[3]-box[0], box[4]-box[1], box[5]-box[2])
    #     fract =dist / l
    #     if most:
    #         fract = fract + 0.5
    #     else:
    #         fract = 0.5 - fract
    #
    # elif len(cross)==4:
    #     pass
    # elif len(cross)==5:
    #     pass
    # elif len(cross)==6:
    #     pass
    # else:
    #     raise ValueError






def splitOctBoxes(box):
    box0 = [box[0], box[1], box[2], (box[0]+box[3])/2.0, (box[1]+box[4])/2.0, (box[2]+box[5])/2.0]
    box1 = [(box[0]+box[3])/2.0, box[1], box[2], box[3], (box[1]+box[4])/2.0, (box[2]+box[5])/2.0]
    box2 = [box[0], (box[1]+box[4])/2.0, box[2], (box[0]+box[3])/2.0, box[4], (box[2]+box[5])/2.0]
    box3 = [(box[0]+box[3])/2.0, (box[1]+box[4])/2.0, box[2], box[3], box[4], (box[2]+box[5])/2.0]
    box4 = [box[0], box[1], (box[2]+box[5])/2.0, (box[0]+box[3])/2.0, (box[1]+box[4])/2.0, box[5]]
    box5 = [(box[0]+box[3])/2.0, box[1], (box[2]+box[5])/2.0, box[3], (box[1]+box[4])/2.0, box[5]]
    box6 = [box[0], (box[1]+box[4])/2.0, (box[2]+box[5])/2.0, (box[0]+box[3])/2.0, box[4], box[5]]
    box7 = [(box[0]+box[3])/2.0, (box[1]+box[4])/2.0, (box[2]+box[5])/2.0, box[3], box[4], box[5]]
    return [box0, box1, box2, box3, box4, box5 ,box6, box7]


class Octree:
    def __init__(self,stl_file, maxLevel = 6, minVolFract = 0.75, cubic=False):
        self.stl_mesh = mesh.Mesh.from_file(stl_file)
        self.triangles = np.append(self.stl_mesh.points.reshape((-1,3,3)), self.stl_mesh.normals.reshape((-1,1,3)),axis=1)
        assert self.triangles.shape[1:]==(4,3)
        if cubic:
            a = max(self.stl_mesh.max_ - self.stl_mesh.min_)
            self.bounding_box = np.append(self.stl_mesh.min_, self.stl_mesh.min_+a)
        else:
            self.bounding_box = np.append(self.stl_mesh.min_, self.stl_mesh.max_)
        assert self.bounding_box.shape==(6,)
        cTriangles, iTriangles, _ = getBoxTriangles(self.triangles, self.bounding_box)
        self.root = Octnode(cTriangles, iTriangles, self.bounding_box, None, "0", maxLevel, minVolFract)

        self.voxelBoxes = None
        self.leafNodes = None


    def traverse(self):
        # 广度优先遍历
        voxelBoxes = []
        voxelNodes = []
        bounding_box = self.root.box
        q = deque()
        q.append(self.root)
        while(q):
            node = q.popleft()
            if not node.isLeaf:
                q.extend(node.branches)
            else:
                voxelBoxes.append(node.box)
                voxelNodes.append(node)
                print("Id {}, ctriangels:{}, itriangles:{}, box:{}".format(node.id, len(node.ctriangles), len(node.itriangles), node.box))
        self.voxelBoxes = voxelBoxes
        self.leafNodes = voxelNodes

    def backtrack(self):
        # 回溯合并节点
        for node in self.leafNodes:
            pnode = node.parent
            while len(pnode.branches)==8:
                pnode.isLeaf=True
                pnode = pnode.parent
        self.traverse()

    def writeBoxes(self, fileName):
        with open(fileName, 'w') as f:
            for box in self.voxelBoxes:
                f.write("{} {} {} {} {} {}\n".format(box[0], box[1], box[2], box[3], box[4], box[5]))



class Octnode:
    def __init__(self, ctriangles, itriangles, bounding_box, parent, id, maxLevel, minVolFract, isLeaf=False):
        self.ctriangles = ctriangles
        self.itriangles = itriangles
        self.box = bounding_box
        self.parent = parent
        self.id = id
        self.maxLevel = maxLevel
        self.minVolFract = minVolFract
        if parent is None:
            self.level = 0
        else:
            self.level = self.parent.level + 1
        self.isLeaf = isLeaf
        self.isFillBox = isLeaf
        # print("Level {}, box:{}".format(self.level, self.box))
        if not isLeaf:
            self.split()


    def checkSplit(self):
        if len(self.itriangles)==0:
            return False

        elif len(self.itriangles)==1:
            if calVolumeFraction(self.itriangles[0], self.box) < self.minVolFract:
                return False
            else:
                return True
        else:
            # 当超过一个三角形与体素盒相交时，继续划分
            return True



    def split(self):
        if self.level==self.maxLevel:
            self.isLeaf = True
            self.branches = None
            return
        if not self.checkSplit():
            self.isLeaf = True
            self.branches = None
            return
        self.branches=[]
        octBoxes = splitOctBoxes(self.box)
        for i,octBox in enumerate(octBoxes):
            if len(self.itriangles)==0:
                ctriangles_, itriangles_, isFill  = getBoxTriangles(self.ctriangles, octBox)
            elif len(self.ctriangles)==0:
                ctriangles_, itriangles_, isFill = getBoxTriangles(self.itriangles, octBox)
            else:
                ctriangles_, itriangles_, isFill = getBoxTriangles(np.append(self.itriangles, self.ctriangles, axis=0), octBox)
            if len(itriangles_)+len(ctriangles_)!=0:
                octnode_ = Octnode(ctriangles_, itriangles_, octBox, self, self.id+"-"+str(i), self.maxLevel, self.minVolFract)
                self.branches.append(octnode_)
            else:
                if isFill:
                    octnode_ = Octnode(ctriangles_, itriangles_, octBox, self, self.id+"-"+str(i), self.maxLevel, self.minVolFract, True)
                    self.branches.append(octnode_)
        assert len(self.branches)!=0




