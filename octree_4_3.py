import numpy as np
from stl import mesh
from collections import deque
import time

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

def checkInterval(v, v1, v2):
    maxv = max(v1,v2)
    minv = min(v1,v2)
    if v>=minv and v<=maxv:
        return True
    else:
        return False

def checkInterWindow_old(point1, point2, window):
    # Cohen–Sutherland clipping algorithm similar
    x1, y1 = point1
    x2, y2 = point2
    TOP = 8 # 1000
    DOWN = 4 # 0100
    RIGHT = 2 # 0010
    LEFT = 1 # 0001

    while True:
        code1 = str((x1 > window[0])*1) + str((x1 < window[1])*1) + str((y1 > window[2])*1) + str((y1 < window[3])*1)
        code2 = str((x2 > window[0])*1) + str((x2 < window[1])*1) + str((y2 > window[2])*1) + str((y2 < window[3])*1)
        # print(code1, code2)
        code1 = int(code1, base=2)
        code2 = int(code2, base=2)
        if (x1-x2)**2+(y1-y2)**2==0:
            return False
        if code1==0 and code2==0:
            return True
        if (code1 & code2) != 0:
            return False
        code = x = y = 0
        if code1==0:
            code=code2
        else:
            code=code1
        if (code & TOP): # point is above the window
            x = window[0]
            y = y1 + (x-x1) * (y2-y1) / (x2-x1)
        elif (code & DOWN): # point is down the window
            x = window[1]
            y = y1 + (x-x1) * (y2-y1) / (x2-x1)
        elif (code & RIGHT): # point is tp the right of the window
            y = window[2]
            x = x1 + (y-y1) * (x2-x1) / (y2-y1)
        elif (code & LEFT): # point is tp the right of the window
            y = window[3]
            x = x1 + (y-y1) * (x2-x1) / (y2-y1)
        else:
            raise ValueError
        if code==code1:
            x1 = x
            y1 = y
        else:
            x2 = x
            y2 = y

def checkInterWindow(point1, point2, window):
    '''
    Liang–Barsky clipping algorithm similar
    x = x1 + t(x2-x1) = x1 + t*deltax
    y = y1 + t(y2-y1) = y1 + t*deltay
    0<=t<=1
    xmin <= x1 + t*deltax <= xmax
    ymin <= y1 + t*deltay <= ymax
    t*pi <= qi
    '''
    p1 = point1[0]-point2[0]
    p2 = -p1
    p3 = point1[1]-point2[1]
    p4 = -p3
    q1 = point1[0] - window[1]
    q2 = window[0] - point1[0]
    q3 = point1[1] - window[3]
    q4 = window[2] - point1[1]
    pos=[1,]
    neg=[0,]
    if p1==0:
        if q1<0 or q2<0 or p3==0:
            return False
    if p3==0:
        if q3<0 or q4<0:
            return False
    if p1!=0:
        r1 = q1 / p1
        r2 = q2 / p2
        if p1 < 0:
            neg.append(r1)
            pos.append(r2)
        else:
            neg.append(r2)
            pos.append(r1)
    if p3!=0:
        r3 = q3 / p3
        r4 = q4 / p4
        if p3 < 0:
            neg.append(r3)
            pos.append(r4)
        else:
            neg.append(r4)
            pos.append(r3)
    u1 = max(neg)
    u2 = min(pos)
    if u1>u2:
        return False
    else:
        return True



def get3DAreaCode(point, box):
    code = str((point[0] > box[3])*1) + str((point[0] < box[0])*1) + str((point[1] > box[4])*1) \
            + str((point[1] < box[1])*1) + str((point[2] > box[5])*1) + str((point[2] < box[2])*1)
    return int(code, base=2)

def get3DBoundCode(point,box):
    code = str((point[0] == box[3])*1) + str((point[0] == box[0])*1) + str((point[1] == box[4])*1) \
            + str((point[1] == box[1])*1) + str((point[2] == box[5])*1) + str((point[2] == box[2])*1)
    return int(code, base=2)

def checkIntersect(triangle, box):
    """
    :param triangle: array, shape=(4,3)
    :param box: list,len=6
    :return: 0 -> not intersect
            1 -> cocincide
            2 -> intersect
    """
    FRONT = 32  # 100000
    BACK = 16 # 010000
    RIGHT = 8 # 001000
    LEFT = 4 # 000100
    TOP = 2 # 000010
    DOWN = 1 # 000001

    code0 = get3DAreaCode(triangle[0,:3], box)
    code1 = get3DAreaCode(triangle[1,:3], box)
    code2 = get3DAreaCode(triangle[2,:3], box)

    bcode0 = get3DBoundCode(triangle[0,:3], box)
    bcode1 = get3DBoundCode(triangle[1,:3], box)
    bcode2 = get3DBoundCode(triangle[2,:3], box)

    if code0==bcode0==0 or code1==bcode1==0 or code2==bcode2==0:
        return 2
    if (code0 & code1 & code2) != 0:
        return 0
    #print(triangle[0])

    while(True):
        if code0==0:
            if (bcode0 & code1 & code2)!=0:
                return 0
            if code1==0:
                if (bcode0 & bcode1 & bcode2)!=0:
                    return 1
                if (bcode0 & code2)!=0:
                    return 0
                else:
                    return 2
            elif code2==0:
                if (bcode0 & code1)!=0:
                    return 0
                else:
                    return 2
            else:
                return 2
        if (code0 & FRONT)!=0:
            x = box[3]
            if (code1 & FRONT) != 0:
                if (triangle[0,0]-triangle[2,0]) * (triangle[1,0]-triangle[2,0])!=0:
                    y1 = triangle[0,1] + (x - triangle[0,0]) * (triangle[0,1]-triangle[2,1]) / (triangle[0,0]-triangle[2,0])
                    z1 = triangle[0,2] + (x - triangle[0,0]) * (triangle[0,2]-triangle[2,2]) / (triangle[0,0]-triangle[2,0])
                    y2 = triangle[1,1] + (x - triangle[1,0]) * (triangle[1,1]-triangle[2,1]) / (triangle[1,0]-triangle[2,0])
                    z2 = triangle[1,2] + (x - triangle[1,0]) * (triangle[1,2]-triangle[2,2]) / (triangle[1,0]-triangle[2,0])
            elif (code2 & FRONT)!=0:
                if (triangle[0,0]-triangle[1,0]) * (triangle[2,0]-triangle[1,0])!=0:
                    y1 = triangle[0,1] + (x - triangle[0,0]) * (triangle[0,1]-triangle[1,1]) / (triangle[0,0]-triangle[1,0])
                    z1 = triangle[0,2] + (x - triangle[0,0]) * (triangle[0,2]-triangle[1,2]) / (triangle[0,0]-triangle[1,0])
                    y2 = triangle[2,1] + (x - triangle[2,0]) * (triangle[2,1]-triangle[1,1]) / (triangle[2,0]-triangle[1,0])
                    z2 = triangle[2,2] + (x - triangle[2,0]) * (triangle[2,2]-triangle[1,2]) / (triangle[2,0]-triangle[1,0])
            else:
                if (triangle[0,0]-triangle[1,0])*(triangle[0,0]-triangle[2,0])!=0:
                    y1 = triangle[0,1] + (x - triangle[0,0]) * (triangle[0,1]-triangle[1,1]) / (triangle[0,0]-triangle[1,0])
                    z1 = triangle[0,2] + (x - triangle[0,0]) * (triangle[0,2]-triangle[1,2]) / (triangle[0,0]-triangle[1,0])
                    y2 = triangle[0,1] + (x - triangle[0,0]) * (triangle[0,1]-triangle[2,1]) / (triangle[0,0]-triangle[2,0])
                    z2 = triangle[0,2] + (x - triangle[0,0]) * (triangle[0,2]-triangle[2,2]) / (triangle[0,0]-triangle[2,0])
            # print("points",y1,z1,y2,z2)
            # print("window",box[4], box[1], box[5], box[2])

            if checkInterWindow([y1,z1], [y2,z2], [box[4], box[1], box[5], box[2]]):
                # print(1)
                break


        if (code0 & BACK)!=0:
            x = box[0]
            if (code1 & BACK)!=0:
                if (triangle[0,0]-triangle[2,0])*(triangle[1,0]-triangle[2,0])!=0:
                    y1 = triangle[0,1] + (x - triangle[0,0]) * (triangle[0,1]-triangle[2,1]) / (triangle[0,0]-triangle[2,0])
                    z1 = triangle[0,2] + (x - triangle[0,0]) * (triangle[0,2]-triangle[2,2]) / (triangle[0,0]-triangle[2,0])
                    y2 = triangle[1,1] + (x - triangle[1,0]) * (triangle[1,1]-triangle[2,1]) / (triangle[1,0]-triangle[2,0])
                    z2 = triangle[1,2] + (x - triangle[1,0]) * (triangle[1,2]-triangle[2,2]) / (triangle[1,0]-triangle[2,0])
            elif (code2 & BACK)!=0:
                if (triangle[0,0]-triangle[1,0])*(triangle[2,0]-triangle[1,0])!=0:
                    y1 = triangle[0,1] + (x - triangle[0,0]) * (triangle[0,1]-triangle[1,1]) / (triangle[0,0]-triangle[1,0])
                    z1 = triangle[0,2] + (x - triangle[0,0]) * (triangle[0,2]-triangle[1,2]) / (triangle[0,0]-triangle[1,0])
                    y2 = triangle[2,1] + (x - triangle[2,0]) * (triangle[2,1]-triangle[1,1]) / (triangle[2,0]-triangle[1,0])
                    z2 = triangle[2,2] + (x - triangle[2,0]) * (triangle[2,2]-triangle[1,2]) / (triangle[2,0]-triangle[1,0])
            else:
                if (triangle[0,0]-triangle[1,0])*(triangle[0,0]-triangle[2,0])!=0:
                    y1 = triangle[0,1] + (x - triangle[0,0]) * (triangle[0,1]-triangle[1,1]) / (triangle[0,0]-triangle[1,0])
                    z1 = triangle[0,2] + (x - triangle[0,0]) * (triangle[0,2]-triangle[1,2]) / (triangle[0,0]-triangle[1,0])
                    y2 = triangle[0,1] + (x - triangle[0,0]) * (triangle[0,1]-triangle[2,1]) / (triangle[0,0]-triangle[2,0])
                    z2 = triangle[0,2] + (x - triangle[0,0]) * (triangle[0,2]-triangle[2,2]) / (triangle[0,0]-triangle[2,0])

            if checkInterWindow([y1,z1], [y2,z2], [box[4], box[1], box[5], box[2]]):
                # print(2)
                break

        if (code0 & RIGHT)!=0:
            y = box[4]
            if (code1 & RIGHT)!=0:
                if (triangle[0,1]-triangle[2,1])*(triangle[1,1]-triangle[2,1])!=0:
                    x1 = triangle[0,0] + (y - triangle[0,1]) * (triangle[0,0]-triangle[2,0]) / (triangle[0,1]-triangle[2,1])
                    z1 = triangle[0,2] + (y - triangle[0,1]) * (triangle[0,2]-triangle[2,2]) / (triangle[0,1]-triangle[2,1])
                    x2 = triangle[1,0] + (y - triangle[1,1]) * (triangle[1,0]-triangle[2,0]) / (triangle[1,1]-triangle[2,1])
                    z2 = triangle[1,2] + (y - triangle[1,1]) * (triangle[1,2]-triangle[2,2]) / (triangle[1,1]-triangle[2,1])
            elif (code2 & RIGHT)!=0:
                if (triangle[0,1]-triangle[1,1])*(triangle[2,1]-triangle[1,1])!=0:
                    x1 = triangle[0,0] + (y - triangle[0,1]) * (triangle[0,0]-triangle[1,0]) / (triangle[0,1]-triangle[1,1])
                    z1 = triangle[0,2] + (y - triangle[0,1]) * (triangle[0,2]-triangle[1,2]) / (triangle[0,1]-triangle[1,1])
                    x2 = triangle[2,0] + (y - triangle[2,1]) * (triangle[2,0]-triangle[1,0]) / (triangle[2,1]-triangle[1,1])
                    z2 = triangle[2,2] + (y - triangle[2,1]) * (triangle[2,2]-triangle[1,2]) / (triangle[2,1]-triangle[1,1])
            else:
                if (triangle[0,1]-triangle[1,1])*(triangle[0,1]-triangle[2,1])!=0:
                    x1 = triangle[0,0] + (y - triangle[0,1]) * (triangle[0,0]-triangle[1,0]) / (triangle[0,1]-triangle[1,1])
                    z1 = triangle[0,2] + (y - triangle[0,1]) * (triangle[0,2]-triangle[1,2]) / (triangle[0,1]-triangle[1,1])
                    x2 = triangle[0,0] + (y - triangle[0,1]) * (triangle[0,0]-triangle[2,0]) / (triangle[0,1]-triangle[2,1])
                    z2 = triangle[0,2] + (y - triangle[0,1]) * (triangle[0,2]-triangle[2,2]) / (triangle[0,1]-triangle[2,1])
            # print("points",x1,z1,x2,z2)
            # print("window",box[3], box[0], box[5], box[2])
            if checkInterWindow([x1,z1], [x2,z2], [box[3], box[0], box[5], box[2]]):
                # print(3)
                break

        if (code0 & LEFT)!=0:
            y = box[1]
            if (code1 & LEFT)!=0:
                if (triangle[0,1]-triangle[2,1])*(triangle[1,1]-triangle[2,1])!=0:
                    x1 = triangle[0,0] + (y - triangle[0,1]) * (triangle[0,0]-triangle[2,0]) / (triangle[0,1]-triangle[2,1])
                    z1 = triangle[0,2] + (y - triangle[0,1]) * (triangle[0,2]-triangle[2,2]) / (triangle[0,1]-triangle[2,1])
                    x2 = triangle[1,0] + (y - triangle[1,1]) * (triangle[1,0]-triangle[2,0]) / (triangle[1,1]-triangle[2,1])
                    z2 = triangle[1,2] + (y - triangle[1,1]) * (triangle[1,2]-triangle[2,2]) / (triangle[1,1]-triangle[2,1])
            elif (code2 & LEFT)!=0:
                if (triangle[0,1]-triangle[1,1])*(triangle[2,1]-triangle[1,1])!=0:
                    x1 = triangle[0,0] + (y - triangle[0,1]) * (triangle[0,0]-triangle[1,0]) / (triangle[0,1]-triangle[1,1])
                    z1 = triangle[0,2] + (y - triangle[0,1]) * (triangle[0,2]-triangle[1,2]) / (triangle[0,1]-triangle[1,1])
                    x2 = triangle[2,0] + (y - triangle[2,1]) * (triangle[2,0]-triangle[1,0]) / (triangle[2,1]-triangle[1,1])
                    z2 = triangle[2,2] + (y - triangle[2,1]) * (triangle[2,2]-triangle[1,2]) / (triangle[2,1]-triangle[1,1])
            else:
                if (triangle[0,1]-triangle[1,1])*(triangle[0,1]-triangle[2,1])!=0:
                    x1 = triangle[0,0] + (y - triangle[0,1]) * (triangle[0,0]-triangle[1,0]) / (triangle[0,1]-triangle[1,1])
                    z1 = triangle[0,2] + (y - triangle[0,1]) * (triangle[0,2]-triangle[1,2]) / (triangle[0,1]-triangle[1,1])
                    x2 = triangle[0,0] + (y - triangle[0,1]) * (triangle[0,0]-triangle[2,0]) / (triangle[0,1]-triangle[2,1])
                    z2 = triangle[0,2] + (y - triangle[0,1]) * (triangle[0,2]-triangle[2,2]) / (triangle[0,1]-triangle[2,1])
            # print("points",x1,z1,x2,z2)
            # print("window",box[3], box[0], box[5], box[2])
            if checkInterWindow([x1,z1], [x2,z2], [box[3], box[0], box[5], box[2]]):
                # print(4)
                break

        if (code0 & TOP)!=0:
            z = box[5]
            if (code1 & TOP)!=0:
                if (triangle[0,2]-triangle[2,2])*(triangle[1,2]-triangle[2,2])!=0:
                    x1 = triangle[0,0] + (z - triangle[0,2]) * (triangle[0,0]-triangle[2,0]) / (triangle[0,2]-triangle[2,2])
                    y1 = triangle[0,1] + (z - triangle[0,2]) * (triangle[0,1]-triangle[2,1]) / (triangle[0,2]-triangle[2,2])
                    x2 = triangle[1,0] + (z - triangle[1,2]) * (triangle[1,0]-triangle[2,0]) / (triangle[1,2]-triangle[2,2])
                    y2 = triangle[1,1] + (z - triangle[1,2]) * (triangle[1,1]-triangle[2,1]) / (triangle[1,2]-triangle[2,2])
            elif (code2 & TOP)!=0:
                if (triangle[0,2]-triangle[1,2])*(triangle[2,2]-triangle[1,2])!=0:
                    x1 = triangle[0,0] + (z - triangle[0,2]) * (triangle[0,0]-triangle[1,0]) / (triangle[0,2]-triangle[1,2])
                    y1 = triangle[0,1] + (z - triangle[0,2]) * (triangle[0,1]-triangle[1,1]) / (triangle[0,2]-triangle[1,2])
                    x2 = triangle[2,0] + (z - triangle[2,2]) * (triangle[2,0]-triangle[1,0]) / (triangle[2,2]-triangle[1,2])
                    y2 = triangle[2,1] + (z - triangle[2,2]) * (triangle[2,1]-triangle[1,1]) / (triangle[2,2]-triangle[1,2])
            else:
                if (triangle[0,2]-triangle[1,2])*(triangle[0,2]-triangle[2,2])!=0:
                    x1 = triangle[0,0] + (z - triangle[0,2]) * (triangle[0,0]-triangle[1,0]) / (triangle[0,2]-triangle[1,2])
                    y1 = triangle[0,1] + (z - triangle[0,2]) * (triangle[0,1]-triangle[1,1]) / (triangle[0,2]-triangle[1,2])
                    x2 = triangle[0,0] + (z - triangle[0,2]) * (triangle[0,0]-triangle[2,0]) / (triangle[0,2]-triangle[2,2])
                    y2 = triangle[0,1] + (z - triangle[0,2]) * (triangle[0,1]-triangle[2,1]) / (triangle[0,2]-triangle[2,2])

            if checkInterWindow([x1,y1], [x2,y2], [box[3], box[0], box[4], box[1]]):
                # print(5)
                break

        if (code0 & DOWN)!=0 and (triangle[0,2]-triangle[1,2])*(triangle[0,2]-triangle[2,2])!=0:
            z = box[2]
            if (code1 & DOWN)!=0:
                if (triangle[0,2]-triangle[2,2])*(triangle[1,2]-triangle[2,2])!=0:
                    x1 = triangle[0,0] + (z - triangle[0,2]) * (triangle[0,0]-triangle[2,0]) / (triangle[0,2]-triangle[2,2])
                    y1 = triangle[0,1] + (z - triangle[0,2]) * (triangle[0,1]-triangle[2,1]) / (triangle[0,2]-triangle[2,2])
                    x2 = triangle[1,0] + (z - triangle[1,2]) * (triangle[1,0]-triangle[2,0]) / (triangle[1,2]-triangle[2,2])
                    y2 = triangle[1,1] + (z - triangle[1,2]) * (triangle[1,1]-triangle[2,1]) / (triangle[1,2]-triangle[2,2])
            elif (code2 & DOWN)!=0:
                if (triangle[0,2]-triangle[1,2])*(triangle[2,2]-triangle[1,2])!=0:
                    x1 = triangle[0,0] + (z - triangle[0,2]) * (triangle[0,0]-triangle[1,0]) / (triangle[0,2]-triangle[1,2])
                    y1 = triangle[0,1] + (z - triangle[0,2]) * (triangle[0,1]-triangle[1,1]) / (triangle[0,2]-triangle[1,2])
                    x2 = triangle[2,0] + (z - triangle[2,2]) * (triangle[2,0]-triangle[1,0]) / (triangle[2,2]-triangle[1,2])
                    y2 = triangle[2,1] + (z - triangle[2,2]) * (triangle[2,1]-triangle[1,1]) / (triangle[2,2]-triangle[1,2])
            else:
                if (triangle[0,2]-triangle[1,2])*(triangle[0,2]-triangle[2,2])!=0:
                    x1 = triangle[0,0] + (z - triangle[0,2]) * (triangle[0,0]-triangle[1,0]) / (triangle[0,2]-triangle[1,2])
                    y1 = triangle[0,1] + (z - triangle[0,2]) * (triangle[0,1]-triangle[1,1]) / (triangle[0,2]-triangle[1,2])
                    x2 = triangle[0,0] + (z - triangle[0,2]) * (triangle[0,0]-triangle[2,0]) / (triangle[0,2]-triangle[2,2])
                    y2 = triangle[0,1] + (z - triangle[0,2]) * (triangle[0,1]-triangle[2,1]) / (triangle[0,2]-triangle[2,2])

            if checkInterWindow([x1,y1], [x2,y2], [box[3], box[0], box[4], box[1]]):
                # print(6)
                break

        return 0

    if (bcode0 & bcode1 & bcode2)!=0:
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
    def __init__(self,stl_file, maxLevel = 6, minLevel = 4, minChildBoxes = 8, cubic=False):
        start = time.time()
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
        self.root = Octnode(cTriangles, iTriangles, self.bounding_box, None, "0", maxLevel, minLevel, minChildBoxes)
        self.voxelBoxes = None
        self.leafNodes = None
        end = time.time()
        print('totally cost(s):',end-start)


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
        print("All {} voxel boxes!".format(len(self.voxelBoxes)))

    def backtrack(self):
        # 回溯合并节点
        for node in self.leafNodes:
            pnode = node.parent
            while pnode!=None and len(pnode.branches)==8:
                merge = True
                for cnode in pnode.branches:
                    if not cnode.isLeaf:
                        merge = False
                        break
                if merge:
                    pnode.isLeaf = True
                    pnode = pnode.parent
                else:
                    break
        self.traverse()

    def writeBoxes(self, fileName):
        with open(fileName, 'w') as f:
            for box in self.voxelBoxes:
                f.write("{} {} {} {} {} {}\n".format(box[0], box[1], box[2], box[3], box[4], box[5]))

    def check(self):
        for node in self.leafNodes:
            if len(node.itriangles)+len(node.ctriangles)==0 and not node.isFillBox:
                print("Error "+node.id)
            if node.box[2]==43.75 and node.box[0]>-1 and node.box[0]<-0 and node.box[1]>-32 and node.box[1]<-31:
                print("Found")
                print("Id {}, ctriangels:{}, itriangles:{}, box:{}".format(node.id, len(node.ctriangles), len(node.itriangles), node.box))
                print(node.itriangles[0])



class Octnode:
    def __init__(self, ctriangles, itriangles, bounding_box, parent, id, maxLevel, minLevel, minChildBoxes, isFillBox=False, isLeaf=False):
        self.ctriangles = ctriangles
        self.itriangles = itriangles
        self.box = bounding_box
        self.parent = parent
        self.id = id
        self.maxLevel = maxLevel
        self.minLevel = minLevel
        self.minChildBoxes = minChildBoxes
        if parent is None:
            self.level = 0
        else:
            self.level = self.parent.level + 1
        self.isLeaf = isLeaf
        self.isFillBox = isFillBox
        self.branches = []
        # print("Level {}, box:{}".format(self.level, self.box))
        if not isLeaf:
            self.split()

    def split(self):
        if self.level==self.maxLevel or len(self.itriangles)==0:
            self.isLeaf = True
            return

        octBoxes = splitOctBoxes(self.box)
        if len(self.itriangles)>1 or self.level < self.minLevel:
            # 当超过一个三角形与体素盒相交时，继续划分
            for i,octBox in enumerate(octBoxes):
                # Split Box
                if len(self.ctriangles)==0:
                    ctriangles_, itriangles_, isFill = getBoxTriangles(self.itriangles, octBox)
                else:
                    ctriangles_, itriangles_, isFill = getBoxTriangles(np.append(self.itriangles, self.ctriangles, axis=0), octBox)
                # Calculate box triangles and Create OctNode
                if len(itriangles_)+len(ctriangles_)!=0 or isFill:
                    octnode_ = Octnode(ctriangles_, itriangles_, octBox, self, self.id+"-"+str(i), self.maxLevel, self.minLevel, self.minChildBoxes, isFillBox=isFill, isLeaf=isFill)
                    self.branches.append(octnode_)
            assert len(self.branches)!=0

        else:
            # 只有一个三角形与体素盒相交
            ctriangles_List = []
            itriangles_List = []
            isFillList = []
            labelList = []
            numOctnodes = 0
            for i,octBox in enumerate(octBoxes):
                # Split Box
                if len(self.ctriangles)==0:
                    ctriangles_, itriangles_, isFill = getBoxTriangles(self.itriangles, octBox)
                else:
                    ctriangles_, itriangles_, isFill = getBoxTriangles(np.append(self.itriangles, self.ctriangles, axis=0), octBox)
                # Calculate box triangles and Create OctNode
                if len(itriangles_)+len(ctriangles_)!=0 or isFill:
                    numOctnodes += 1
                    ctriangles_List.append(ctriangles_)
                    itriangles_List.append(itriangles_)
                    isFillList.append(isFill)
                    labelList.append(i)
            if numOctnodes < self.minChildBoxes:
                for i in range(numOctnodes):
                    octnode_ = Octnode(ctriangles_List[i], itriangles_List[i], octBoxes[labelList[i]], self, self.id+"-"+str(labelList[i]), self.maxLevel, self.minLevel, self.minChildBoxes, isFillBox=isFillList[i], isLeaf=isFillList[i])
                    self.branches.append(octnode_)
            else:
                self.isLeaf = True
                self.branches = None









