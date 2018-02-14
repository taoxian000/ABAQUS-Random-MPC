# -*- coding: utf-8 -*-
#filename:abaqus_1.py
#######################################设定参数
if os.path.exists('D:\\PythonCode\\bishe\\ellipse_force.txt'):
    os.remove('D:\\PythonCode\\bishe\\ellipse_force.txt')

f = open('D:\\PythonCode\\bishe\\ellipse.txt','r')
ffo = open('D:\\PythonCode\\bishe\\ellipse_force.txt','a+')
ffo.write('name\t\tRF1\t\tU1\t\tRF2\t\tU2\n')
#i=0
for line in f:
    #i=i+1
    #print (i)
    data=line.split()
    bwidx=float(data[0])    #基体宽度
    bwidy=float(data[1])    #基体长度
    f_len=float(data[2])    #纤维长度
    f_wid=float(data[3])    #纤维宽度
    f_dis=float(data[4])    #纤维最小间距
    f_num=int(data[5])      #纤维数目
    size0=float(data[6])    #网格尺寸
    job_name=data[7]        #工作名称
    Pathname=data[8]        #存储路径
    
    ####################################调用模块
    from random import *
    from abaqus import *
    from abaqusConstants import *
    from caeModules import *
    from driverUtils import executeOnCaeStartup
    from abaqus import backwardCompatibility
    backwardCompatibility.setValues(reportDeprecated=False)
    executeOnCaeStartup()
    import math
    import os
    os.chdir(Pathname)
    
    from math import *
    L=bwidx       #基体长度
    B=bwidy       #基体宽度 
    f_num_new=0   #计入被边界截断的纤维数目
    f_len_temp=f_len+f_dis    #较粗大纤维长度，用以确保纤维之间距离不能太小
    f_wid_temp=f_wid+f_dis    #较粗大纤维宽度，用以确保纤维之间距离不能太小
    fiber_vertices=[[]]       #创建矩阵存储纤维编号和四个顶点坐标
    del fiber_vertices[0]
    fiber_vertices_temp=[[]]  #创建临时矩阵存储较宽的纤维编号和四个顶点坐标，用以确保纤维之间距离不能太小
    del fiber_vertices_temp[0]
    #####
    #####点到点的距离
    def disd(vertice1,vertice2):
        dis=sqrt((vertice2[1]-vertice1[1])**2+(vertice2[0]-vertice1[0])**2)
        return dis
    
    #####
    #####点到直线的距离
    def disl(vertice,edgev1,edgev2):
        k=(edgev2[1]-edgev1[1])/(edgev2[0]-edgev1[0])
        b=edgev1[1]-k*edgev1[0]
        #leng=0-(b**2/k/sqrt(b**2+b**2/k**2))
        #edge=[edgev2[1]-edgev1[1],edgev2[0]-edgev1[0]]
        #OA=doc(vertice,edge)/sqrt(edge[0]**2+edge[1]**2)
        #del edge
        #dis=sqrt(vertice[0]**2+vertice[1]**2-OA**2)+abs(leng)
        dis = abs((vertice[1]-k*vertice[0]-b)/sqrt(k**2+1))
        return dis
    
    #####
    #####点和向量点乘
    def doc(vertice,edge):
        axis=[edge[0]/sqrt(edge[0]**2+edge[1]**2),edge[1]/sqrt(edge[0]**2+edge[1]**2)]
        doc=vertice[0]*edge[0]+vertice[1]*edge[1]
        return doc
    
    #####
    #####两根纤维是否发生交叉
    def overlap(fiber1,fiber2):
        vertices1=[[]]
        vertices2=[[]]
        edge=[[]]
        del vertices1[0]
        del vertices2[0]
        del edge[0]
        for i in range(4):      #####找出两个矩形八个顶点
            vertices1.append([fiber1[1+2*i],fiber1[2+2*i]])
        for i in range(4):
            vertices2.append([fiber2[1+2*i],fiber2[2+2*i]])
        for i in range(2):     ######找出两个矩形四条投影边
            edge.append([vertices1[i+1][0]-vertices1[i][0],vertices1[i+1][1]-vertices1[i][1]])
        for i in range(2):
            edge.append([vertices2[i+1][0]-vertices2[i][0],vertices2[i+1][1]-vertices2[i][1]])
        non_cross=[]
        if abs(disd([fiber1[1],fiber1[2]],[fiber1[3],fiber1[4]])-f_wid)<f_wid:
            x_ShortL1=(fiber1[1]+fiber1[3])/2
            x_ShortR1=(fiber1[5]+fiber1[7])/2
            y_ShortL1=(fiber1[2]+fiber1[4])/2
            y_ShortR1=(fiber1[6]+fiber1[8])/2
        elif abs(disd([fiber1[1],fiber1[2]],[fiber1[7],fiber1[8]])-f_wid)<f_wid:
            x_ShortL1=(fiber1[1]+fiber1[7])/2
            x_ShortR1=(fiber1[3]+fiber1[5])/2
            y_ShortL1=(fiber1[2]+fiber1[8])/2
            y_ShortR1=(fiber1[4]+fiber1[6])/2
        elif abs(disd([fiber1[1],fiber1[2]],[fiber1[5],fiber1[6]])-f_wid)<f_wid:
            x_ShortL1=(fiber1[1]+fiber1[5])/2
            x_ShortR1=(fiber1[3]+fiber1[7])/2
            y_ShortL1=(fiber1[2]+fiber1[6])/2
            y_ShortR1=(fiber1[4]+fiber1[8])/2
        if abs(disd([fiber2[1],fiber2[2]],[fiber2[3],fiber2[4]])-f_wid)<f_wid:
            x_ShortL2=(fiber2[1]+fiber2[3])/2
            x_ShortR2=(fiber2[5]+fiber2[7])/2
            y_ShortL2=(fiber2[2]+fiber2[4])/2
            y_ShortR2=(fiber2[6]+fiber2[8])/2
        elif abs(disd([fiber2[1],fiber2[2]],[fiber2[7],fiber2[8]])-f_wid)<f_wid:
            x_ShortL2=(fiber2[1]+fiber2[7])/2
            x_ShortR2=(fiber2[3]+fiber2[5])/2
            y_ShortL2=(fiber2[2]+fiber2[8])/2
            y_ShortR2=(fiber2[4]+fiber2[6])/2
        elif abs(disd([fiber2[1],fiber2[2]],[fiber2[5],fiber2[6]])-f_wid)<f_wid:
            x_ShortL2=(fiber2[1]+fiber2[5])/2
            x_ShortR2=(fiber2[3]+fiber2[7])/2
            y_ShortL2=(fiber2[2]+fiber2[6])/2
            y_ShortR2=(fiber2[4]+fiber2[8])/2
        
        x1 = (fiber1[1]+fiber1[5])/2
        y1 = (fiber1[2]+fiber1[6])/2
        x2 = (fiber2[1]+fiber2[5])/2
        y2 = (fiber2[2]+fiber2[6])/2
        
        d1 = disl([x1, y1], [x2, y2], [x_ShortR2, y_ShortR2])
        d2 = disl([x2, y2], [x1, y1], [x_ShortR1, y_ShortR1])
        
        if disd([x1, y1], [x2, y2]) > 1.415*f_len+f_dis:
            return 0
        elif d1 < 0.4*f_len and d2 < 0.4*f_len:
            return 1
        elif d2 > f_wid+f_dis:
            k1 = (y_ShortR1-y1) / (x_ShortR1-x1)
            b1 = y1 - k1 * x1
            k2 = (y_ShortR2-y2) / (x_ShortR2-x2)
            b2 = y2 - k2 * x2
            xc = (b2-b1)/(k1-k2)
            yc = k1 * xc + b1
            if abs(k1 - k2) < 0.1:
                return 0
            if disd([xc, yc], [x2, y2]) > 0.5*f_len+0.75*f_wid+f_dis:
                return 0
            else:
                return 1
        elif d1 > f_wid+f_dis:
            k1 = (y_ShortR1-y1) / (x_ShortR1-x1)
            b1 = y1 - k1 * x1
            k2 = (y_ShortR2-y2) / (x_ShortR2-x2)
            b2 = y2 - k2 * x2
            xc = (b2-b1)/(k1-k2)
            yc = k1 * xc + b1
            if abs(k1 - k2) < 0.1:
                return 0
            if disd([xc, yc], [x1, y1]) > 0.5*f_len+0.75*f_wid+f_dis:
                return 0
            else:
                return 1
        else:
            return 1
    
    #####
    #####纤维生成
    for i in range(1,f_num+1):
        print(i)
        do=0       #判断纤维是否生成成功
        while do==0:
            x_m=L*random()
            y_m=L*random()
            angle=pi*gauss(0,23.4)/180
            x_L=x_m-f_len/2*cos(angle)
            y_L=y_m-f_len/2*sin(angle)
            x_R=x_m+f_len/2*cos(angle)
            y_R=y_m+f_len/2*sin(angle)
            x_L_temp=x_m-f_len_temp/2*cos(angle)
            y_L_temp=y_m-f_len_temp/2*sin(angle)
            x_R_temp=x_m+f_len_temp/2*cos(angle)
            y_R_temp=y_m+f_len_temp/2*sin(angle)
            if TRUE:
                if angle==0 or angle==pi/2 or angle==-pi/2 or angle==pi/4 or angle==-pi/4:
                    continue
                else:
                    k_=tan(angle)
                    x_LR=x_m-(k_*k_*f_wid/abs(sin(angle))-f_len/abs(cos(angle)))/2/(k_*k_+1)
                    y_LR=y_m+k_*(f_len/abs(cos(angle))+f_wid/abs(sin(angle)))/2/(k_*k_+1)
                    x_LL=x_m-(k_*k_*f_wid/abs(sin(angle))+f_len/abs(cos(angle)))/2/(k_*k_+1)
                    y_LL=y_m-k_*(f_len/abs(cos(angle))-f_wid/abs(sin(angle)))/2/(k_*k_+1)
                    x_RR=x_m+(k_*k_*f_wid/abs(sin(angle))+f_len/abs(cos(angle)))/2/(k_*k_+1)
                    y_RR=y_m+k_*(f_len/abs(cos(angle))-f_wid/abs(sin(angle)))/2/(k_*k_+1)
                    x_RL=x_m+(k_*k_*f_wid/abs(sin(angle))-f_len/abs(cos(angle)))/2/(k_*k_+1)
                    y_RL=y_m-k_*(f_len/abs(cos(angle))+f_wid/abs(sin(angle)))/2/(k_*k_+1)
                    x_LR_temp=x_m-(k_*k_*f_wid_temp/abs(sin(angle))-f_len_temp/abs(cos(angle)))/2/(k_*k_+1)
                    y_LR_temp=y_m+k_*(f_len_temp/abs(cos(angle))+f_wid_temp/abs(sin(angle)))/2/(k_*k_+1)
                    x_LL_temp=x_m-(k_*k_*f_wid_temp/abs(sin(angle))+f_len_temp/abs(cos(angle)))/2/(k_*k_+1)
                    y_LL_temp=y_m-k_*(f_len_temp/abs(cos(angle))-f_wid_temp/abs(sin(angle)))/2/(k_*k_+1)
                    x_RR_temp=x_m+(k_*k_*f_wid_temp/abs(sin(angle))+f_len_temp/abs(cos(angle)))/2/(k_*k_+1)
                    y_RR_temp=y_m+k_*(f_len_temp/abs(cos(angle))-f_wid_temp/abs(sin(angle)))/2/(k_*k_+1)
                    x_RL_temp=x_m+(k_*k_*f_wid_temp/abs(sin(angle))-f_len_temp/abs(cos(angle)))/2/(k_*k_+1)
                    y_RL_temp=y_m-k_*(f_len_temp/abs(cos(angle))+f_wid_temp/abs(sin(angle)))/2/(k_*k_+1)            
                    if min(x_LL,x_RL)<=0 and min(y_LL,y_RL,y_LR,y_RR)<=0:
                        continue
                    elif min(x_LL,x_RL)<=0 and max(y_LL,y_RL,y_LR,y_RR)>=L:
                        continue
                    elif max(x_RR,x_LR)-L>=0 and min(y_LL,y_RL,y_LR,y_RR)<=0:
                        continue
                    elif max(x_RR,x_LR)-L>=0 and max(y_LL,y_RL,y_LR,y_RR)>=L:
                        continue
                    elif min(x_LL,x_RL)>=0 and max(x_LR,x_RR)<=L and min(y_LL,y_RL,y_LR,y_RR)>=0 and max(y_LL,y_RL,y_LR,y_RR)<=L:    #纤维与边界无交点           
                        if k_>0:     
                            cross=[]
                            if len(fiber_vertices)==0:
                                fiber_vertices.append([i,x_LL,y_LL,x_RL,y_RL,x_RR,y_RR,x_LR,y_LR])
                                fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp,x_RL_temp,y_RL_temp,x_RR_temp,y_RR_temp,x_LR_temp,y_LR_temp])
                                break
                            else:
                                temp=[i,x_LL_temp,y_LL_temp,x_RL_temp,y_RL_temp,x_RR_temp,y_RR_temp,x_LR_temp,y_LR_temp]
                                for j in range(len(fiber_vertices_temp)):
                                    cross.append(overlap(fiber_vertices_temp[j],temp))
                                if max(cross)==1:
                                    del cross
                                    continue
                                else:
                                    fiber_vertices.append([i,x_LL,y_LL,x_RL,y_RL,x_RR,y_RR,x_LR,y_LR])
                                    fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp,x_RL_temp,y_RL_temp,x_RR_temp,y_RR_temp,x_LR_temp,y_LR_temp])
                                    del cross
                                    break
                        else:
                            cross=[]
                            if len(fiber_vertices)==0:
                                fiber_vertices.append([i,x_LL,y_LL,x_LR,y_LR,x_RR,y_RR,x_RL,y_RL])
                                fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp,x_LR_temp,y_LR_temp,x_RR_temp,y_RR_temp,x_RL_temp,y_RL_temp])
                                break
                            else:
                                temp=[i,x_LL_temp,y_LL_temp,x_LR_temp,y_LR_temp,x_RR_temp,y_RR_temp,x_RL_temp,y_RL_temp]
                                for j in range(len(fiber_vertices_temp)):
                                    cross.append(overlap(fiber_vertices_temp[j],temp))
                                if max(cross)==1:
                                    del cross
                                    continue
                                else:
                                    fiber_vertices.append([i,x_LL,y_LL,x_LR,y_LR,x_RR,y_RR,x_RL,y_RL])
                                    fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp,x_LR_temp,y_LR_temp,x_RR_temp,y_RR_temp,x_RL_temp,y_RL_temp])
                                    del cross
                                    break                    
                    elif max(x_LL,x_RL)<0 and min(x_LR,x_RR)>0:    #纤维与左边界有交点
                        if k_>0:
                            cross=[]                     
                            if len(fiber_vertices)==0:
                                fiber_vertices.append([i,x_LL,y_LL,x_RL,y_RL,x_RR,y_RR,x_LR,y_LR])
                                fiber_vertices.append([i,x_LL+L,y_LL,x_RL+L,y_RL,x_RR+L,y_RR,x_LR+L,y_LR])
                                fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp,x_RL_temp,y_RL_temp,x_RR_temp,y_RR_temp,x_LR_temp,y_LR_temp])
                                fiber_vertices_temp.append([i,x_LL_temp+L,y_LL_temp,x_RL_temp+L,y_RL_temp,x_RR_temp+L,y_RR_temp,x_LR_temp+L,y_LR_temp])                        
                                break
                            else:
                                temp1=[i,x_LL_temp,y_LL_temp,x_RL_temp,y_RL_temp,x_RR_temp,y_RR_temp,x_LR_temp,y_LR_temp]
                                for j in range(len(fiber_vertices_temp)):
                                    cross.append(overlap(fiber_vertices_temp[j],temp1))
                                temp2=[i,x_LL_temp+L,y_LL_temp,x_RL_temp+L,y_RL_temp,x_RR_temp+L,y_RR_temp,x_LR_temp+L,y_LR_temp]
                                for j in range(len(fiber_vertices_temp)):
                                    cross.append(overlap(fiber_vertices_temp[j],temp2))                        
                                if max(cross)==1:
                                    del cross
                                    continue
                                else:
                                    fiber_vertices.append([i,x_LL,y_LL,x_RL,y_RL,x_RR,y_RR,x_LR,y_LR])
                                    fiber_vertices.append([i,x_LL+L,y_LL,x_RL+L,y_RL,x_RR+L,y_RR,x_LR+L,y_LR])
                                    fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp,x_RL_temp,y_RL_temp,x_RR_temp,y_RR_temp,x_LR_temp,y_LR_temp])
                                    fiber_vertices_temp.append([i,x_LL_temp+L,y_LL_temp,x_RL_temp+L,y_RL_temp,x_RR_temp+L,y_RR_temp,x_LR_temp+L,y_LR_temp])                                 
                                    del cross
                                    break
                        else:
                            cross=[]                    
                            if len(fiber_vertices)==0:
                                fiber_vertices.append([i,x_LL,y_LL,x_LR,y_LR,x_RR,y_RR,x_RL,y_RL])
                                fiber_vertices.append([i,x_LL+L,y_LL,x_LR+L,y_LR,x_RR+L,y_RR,x_RL+L,y_RL])
                                fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp,x_LR_temp,y_LR_temp,x_RR_temp,y_RR_temp,x_RL_temp,y_RL_temp])
                                fiber_vertices_temp.append([i,x_LL_temp+L,y_LL_temp,x_LR_temp+L,y_LR_temp,x_RR_temp+L,y_RR_temp,x_RL_temp+L,y_RL_temp])                        
                                break
                            else:
                                temp1=[i,x_LL_temp,y_LL_temp,x_LR_temp,y_LR_temp,x_RR_temp,y_RR_temp,x_RL_temp,y_RL_temp]
                                for j in range(len(fiber_vertices_temp)):
                                    cross.append(overlap(fiber_vertices_temp[j],temp1))
                                temp2=[i,x_LL_temp+L,y_LL_temp,x_LR_temp+L,y_LR_temp,x_RR_temp+L,y_RR_temp,x_RL_temp+L,y_RL_temp]
                                for j in range(len(fiber_vertices_temp)):
                                    cross.append(overlap(fiber_vertices_temp[j],temp2))                        
                                if max(cross)==1:
                                    del cross
                                    continue
                                else:
                                    fiber_vertices.append([i,x_LL,y_LL,x_LR,y_LR,x_RR,y_RR,x_RL,y_RL])
                                    fiber_vertices.append([i,x_LL+L,y_LL,x_LR+L,y_LR,x_RR+L,y_RR,x_RL+L,y_RL])
                                    fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp,x_LR_temp,y_LR_temp,x_RR_temp,y_RR_temp,x_RL_temp,y_RL_temp])
                                    fiber_vertices_temp.append([i,x_LL_temp+L,y_LL_temp,x_LR_temp+L,y_LR_temp,x_RR_temp+L,y_RR_temp,x_RL_temp+L,y_RL_temp])                             
                                    del cross
                                    break                                                                  
                    elif max(x_LL,x_RL)<L and min(x_LR,x_RR)>L:    #纤维与右边界有交点
                        if k_>0:
                            cross=[]
                            if len(fiber_vertices)==0:
                                fiber_vertices.append([i,x_LL,y_LL,x_RL,y_RL,x_RR,y_RR,x_LR,y_LR])
                                fiber_vertices.append([i,x_LL-L,y_LL,x_RL-L,y_RL,x_RR-L,y_RR,x_LR-L,y_LR])
                                fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp,x_RL_temp,y_RL_temp,x_RR_temp,y_RR_temp,x_LR_temp,y_LR_temp])
                                fiber_vertices_temp.append([i,x_LL_temp-L,y_LL_temp,x_RL_temp-L,y_RL_temp,x_RR_temp-L,y_RR_temp,x_LR_temp-L,y_LR_temp])                        
                                break
                            else:
                                temp1=[i,x_LL_temp,y_LL_temp,x_RL_temp,y_RL_temp,x_RR_temp,y_RR_temp,x_LR_temp,y_LR_temp]
                                for j in range(len(fiber_vertices_temp)):
                                    cross.append(overlap(fiber_vertices_temp[j],temp1))
                                temp2=[i,x_LL_temp-L,y_LL_temp,x_RL_temp-L,y_RL_temp,x_RR_temp-L,y_RR_temp,x_LR_temp-L,y_LR_temp]
                                for j in range(len(fiber_vertices_temp)):
                                    cross.append(overlap(fiber_vertices_temp[j],temp2))                        
                                if max(cross)==1:
                                    del cross
                                    continue
                                else:
                                    fiber_vertices.append([i,x_LL,y_LL,x_RL,y_RL,x_RR,y_RR,x_LR,y_LR])
                                    fiber_vertices.append([i,x_LL-L,y_LL,x_RL-L,y_RL,x_RR-L,y_RR,x_LR-L,y_LR])
                                    fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp,x_RL_temp,y_RL_temp,x_RR_temp,y_RR_temp,x_LR_temp,y_LR_temp])
                                    fiber_vertices_temp.append([i,x_LL_temp-L,y_LL_temp,x_RL_temp-L,y_RL_temp,x_RR_temp-L,y_RR_temp,x_LR_temp-L,y_LR_temp])                               
                                    del cross
                                    break
                        else:
                            cross=[]
                            if len(fiber_vertices)==0:
                                fiber_vertices.append([i,x_LL,y_LL,x_LR,y_LR,x_RR,y_RR,x_RL,y_RL])
                                fiber_vertices.append([i,x_LL-L,y_LL,x_LR-L,y_LR,x_RR-L,y_RR,x_RL-L,y_RL])
                                fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp,x_LR_temp,y_LR_temp,x_RR_temp,y_RR_temp,x_RL_temp,y_RL_temp])
                                fiber_vertices_temp.append([i,x_LL_temp-L,y_LL_temp,x_LR_temp-L,y_LR_temp,x_RR_temp-L,y_RR_temp,x_RL_temp-L,y_RL_temp])                               
                                break
                            else:
                                temp1=[i,x_LL_temp,y_LL_temp,x_LR_temp,y_LR_temp,x_RR_temp,y_RR_temp,x_RL_temp,y_RL_temp]
                                for j in range(len(fiber_vertices_temp)):
                                    cross.append(overlap(fiber_vertices_temp[j],temp1))
                                temp2=[i,x_LL_temp-L,y_LL_temp,x_LR_temp-L,y_LR_temp,x_RR_temp-L,y_RR_temp,x_RL_temp-L,y_RL_temp]
                                for j in range(len(fiber_vertices_temp)):
                                    cross.append(overlap(fiber_vertices_temp[j],temp2))                        
                                if max(cross)==1:
                                    del cross
                                    continue
                                else:
                                    fiber_vertices.append([i,x_LL,y_LL,x_LR,y_LR,x_RR,y_RR,x_RL,y_RL])
                                    fiber_vertices.append([i,x_LL-L,y_LL,x_LR-L,y_LR,x_RR-L,y_RR,x_RL-L,y_RL])
                                    fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp,x_LR_temp,y_LR_temp,x_RR_temp,y_RR_temp,x_RL_temp,y_RL_temp])
                                    fiber_vertices_temp.append([i,x_LL_temp-L,y_LL_temp,x_LR_temp-L,y_LR_temp,x_RR_temp-L,y_RR_temp,x_RL_temp-L,y_RL_temp])                                 
                                    del cross
                                    break                               
                    elif max(y_LL,y_RL)<L and min(y_LR,y_RR)>L:    #纤维与上边界有交点
                        if k_>0:
                            cross=[]
                            if len(fiber_vertices)==0:
                                fiber_vertices.append([i,x_LL,y_LL,x_RL,y_RL,x_RR,y_RR,x_LR,y_LR])
                                fiber_vertices.append([i,x_LL,y_LL-L,x_RL,y_RL-L,x_RR,y_RR-L,x_LR,y_LR-L])
                                fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp,x_RL_temp,y_RL_temp,x_RR_temp,y_RR_temp,x_LR_temp,y_LR_temp])
                                fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp-L,x_RL_temp,y_RL_temp-L,x_RR_temp,y_RR_temp-L,x_LR_temp,y_LR_temp-L])                               
                                break
                            else:
                                temp1=[i,x_LL_temp,y_LL_temp,x_RL_temp,y_RL_temp,x_RR_temp,y_RR_temp,x_LR_temp,y_LR_temp]
                                for j in range(len(fiber_vertices_temp)):
                                    cross.append(overlap(fiber_vertices_temp[j],temp1))
                                temp2=[i,x_LL_temp,y_LL_temp-L,x_RL_temp,y_RL_temp-L,x_RR_temp,y_RR_temp-L,x_LR_temp,y_LR_temp-L]
                                for j in range(len(fiber_vertices_temp)):
                                    cross.append(overlap(fiber_vertices_temp[j],temp2))                        
                                if max(cross)==1:
                                    del cross
                                    continue
                                else:
                                    fiber_vertices.append([i,x_LL,y_LL,x_RL,y_RL,x_RR,y_RR,x_LR,y_LR])
                                    fiber_vertices.append([i,x_LL,y_LL-L,x_RL,y_RL-L,x_RR,y_RR-L,x_LR,y_LR-L])
                                    fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp,x_RL_temp,y_RL_temp,x_RR_temp,y_RR_temp,x_LR_temp,y_LR_temp])
                                    fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp-L,x_RL_temp,y_RL_temp-L,x_RR_temp,y_RR_temp-L,x_LR_temp,y_LR_temp-L])                                
                                    del cross
                                    break
                        else:
                            cross=[]
                            if len(fiber_vertices)==0:
                                fiber_vertices.append([i,x_LL,y_LL,x_LR,y_LR,x_RR,y_RR,x_RL,y_RL])
                                fiber_vertices.append([i,x_LL,y_LL-L,x_LR,y_LR-L,x_RR,y_RR-L,x_RL,y_RL-L])
                                fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp,x_LR_temp,y_LR_temp,x_RR_temp,y_RR_temp,x_RL_temp,y_RL_temp])
                                fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp-L,x_LR_temp,y_LR_temp-L,x_RR_temp,y_RR_temp-L,x_RL_temp,y_RL_temp-L])                               
                                break
                            else:
                                temp1=[i,x_LL_temp,y_LL_temp,x_LR_temp,y_LR_temp,x_RR_temp,y_RR_temp,x_RL_temp,y_RL_temp]
                                for j in range(len(fiber_vertices_temp)):
                                    cross.append(overlap(fiber_vertices_temp[j],temp1))
                                temp2=[i,x_LL_temp,y_LL_temp-L,x_LR_temp,y_LR_temp-L,x_RR_temp,y_RR_temp-L,x_RL_temp,y_RL_temp-L]
                                for j in range(len(fiber_vertices_temp)):
                                    cross.append(overlap(fiber_vertices_temp[j],temp2))                        
                                if max(cross)==1:
                                    del cross
                                    continue
                                else:
                                    fiber_vertices.append([i,x_LL,y_LL,x_LR,y_LR,x_RR,y_RR,x_RL,y_RL])
                                    fiber_vertices.append([i,x_LL,y_LL-L,x_LR,y_LR-L,x_RR,y_RR-L,x_RL,y_RL-L])
                                    fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp,x_LR_temp,y_LR_temp,x_RR_temp,y_RR_temp,x_RL_temp,y_RL_temp])
                                    fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp-L,x_LR_temp,y_LR_temp-L,x_RR_temp,y_RR_temp-L,x_RL_temp,y_RL_temp-L])                                 
                                    del cross
                                    break                    
                    elif max(y_LL,y_RL)<0 and min(y_LR,y_RR)>0:    #纤维与下边界有交点
                        if k_>0:
                            cross=[]
                            if len(fiber_vertices)==0:
                                fiber_vertices.append([i,x_LL,y_LL,x_RL,y_RL,x_RR,y_RR,x_LR,y_LR])
                                fiber_vertices.append([i,x_LL,y_LL+L,x_RL,y_RL+L,x_RR,y_RR+L,x_LR,y_LR+L])
                                fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp,x_RL_temp,y_RL_temp,x_RR_temp,y_RR_temp,x_LR_temp,y_LR_temp])
                                fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp+L,x_RL_temp,y_RL_temp+L,x_RR_temp,y_RR_temp+L,x_LR_temp,y_LR_temp+L])                               
                                break
                            else:
                                temp1=[i,x_LL_temp,y_LL_temp,x_RL_temp,y_RL_temp,x_RR_temp,y_RR_temp,x_LR_temp,y_LR_temp]
                                for j in range(len(fiber_vertices_temp)):
                                    cross.append(overlap(fiber_vertices_temp[j],temp1))
                                temp2=[i,x_LL_temp,y_LL_temp+L,x_RL_temp,y_RL_temp+L,x_RR_temp,y_RR_temp+L,x_LR_temp,y_LR_temp+L]
                                for j in range(len(fiber_vertices_temp)):
                                    cross.append(overlap(fiber_vertices_temp[j],temp2))                        
                                if max(cross)==1:
                                    del cross
                                    continue
                                else:
                                    fiber_vertices.append([i,x_LL,y_LL,x_RL,y_RL,x_RR,y_RR,x_LR,y_LR])
                                    fiber_vertices.append([i,x_LL,y_LL+L,x_RL,y_RL+L,x_RR,y_RR+L,x_LR,y_LR+L])
                                    fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp,x_RL_temp,y_RL_temp,x_RR_temp,y_RR_temp,x_LR_temp,y_LR_temp])
                                    fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp+L,x_RL_temp,y_RL_temp+L,x_RR_temp,y_RR_temp+L,x_LR_temp,y_LR_temp+L])                                
                                    del cross
                                    break
                        else:
                            cross=[]
                            if len(fiber_vertices)==0:
                                fiber_vertices.append([i,x_LL,y_LL,x_LR,y_LR,x_RR,y_RR,x_RL,y_RL])
                                fiber_vertices.append([i,x_LL,y_LL+L,x_LR,y_LR+L,x_RR,y_RR+L,x_RL,y_RL+L])
                                fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp,x_LR_temp,y_LR_temp,x_RR_temp,y_RR_temp,x_RL_temp,y_RL_temp])
                                fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp+L,x_LR_temp,y_LR_temp+L,x_RR_temp,y_RR_temp+L,x_RL_temp,y_RL_temp+L])                               
                                break
                            else:
                                temp1=[i,x_LL_temp,y_LL_temp,x_LR_temp,y_LR_temp,x_RR_temp,y_RR_temp,x_RL_temp,y_RL_temp]
                                for j in range(len(fiber_vertices_temp)):
                                    cross.append(overlap(fiber_vertices_temp[j],temp1))
                                temp2=[i,x_LL_temp,y_LL_temp+L,x_LR_temp,y_LR_temp+L,x_RR_temp,y_RR_temp+L,x_RL_temp,y_RL_temp+L]
                                for j in range(len(fiber_vertices_temp)):
                                    cross.append(overlap(fiber_vertices_temp[j],temp2))                        
                                if max(cross)==1:
                                    del cross
                                    continue
                                else:
                                    fiber_vertices.append([i,x_LL,y_LL,x_LR,y_LR,x_RR,y_RR,x_RL,y_RL])
                                    fiber_vertices.append([i,x_LL,y_LL+L,x_LR,y_LR+L,x_RR,y_RR+L,x_RL,y_RL+L])
                                    fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp,x_LR_temp,y_LR_temp,x_RR_temp,y_RR_temp,x_RL_temp,y_RL_temp])
                                    fiber_vertices_temp.append([i,x_LL_temp,y_LL_temp+L,x_LR_temp,y_LR_temp+L,x_RR_temp,y_RR_temp+L,x_RL_temp,y_RL_temp+L])                                
                                    del cross
                                    break                                                 
                    else:
                        continue
            #except:
            #    print 'wrong'
    ##############################开始建模
    
    try:
        Mdb()
        from part import *     #第一步, 建立建模
        s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1000.0)   #定义模型的草图s
        s.rectangle(point1=(0.0, 0.0), point2=(bwidx, bwidy))                   #指定两顶点画矩形
        p = mdb.models['Model-1'].Part(name='Part-1',dimensionality=TWO_D_PLANAR,type=DEFORMABLE_BODY)   #定义模型的部件part-1
        p.BaseShell(sketch=s)                                                        #将s赋给p
        del mdb.models['Model-1'].sketches['__profile__']   #收回建模所占的环境内存
        
        s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1000.0)
        g = s1.geometry
        fr = open('D:\\PythonCode\\bishe\\result_ellipse.txt','w+')
        fr.write('CenterX\t\t\tCenterY\t\t\tAngle\n')
        for i in range(len(fiber_vertices)):
            s1.EllipseByCenterPerimeter(center=((fiber_vertices[i][1]+fiber_vertices[i][5])/2,(fiber_vertices[i][2]+fiber_vertices[i][6])/2), 
                axisPoint1=((fiber_vertices[i][3]+fiber_vertices[i][5])/2,(fiber_vertices[i][4]+fiber_vertices[i][6])/2), 
                axisPoint2=((fiber_vertices[i][1]+fiber_vertices[i][3])/2,(fiber_vertices[i][2]+fiber_vertices[i][4])/2))
            fr.write(str((fiber_vertices[i][1]+fiber_vertices[i][5])/2)+'\t'+str((fiber_vertices[i][2]+fiber_vertices[i][6])/2)+'\t')
            fr.write(str(180/pi*atan((fiber_vertices[i][4]-fiber_vertices[i][6])/(fiber_vertices[i][3]-fiber_vertices[i][5])))+'\n')
        
        fr.close()
        p1 = mdb.models['Model-1'].parts['Part-1']
        pickedFaces = p1.faces[0:1]
        p1.PartitionFaceBySketch(faces=pickedFaces, sketch=s1)
        mdb.models['Model-1'].convertAllSketches()
        
        from material import *      #第二步, 材料定义
        from section import *
        mdb.models['Model-1'].Material(name='MATRIX')   #定义材料名称1
        mdb.models['Model-1'].materials['MATRIX'].Elastic(dependencies=2, table=((1100, 
            0.38, 0.0, 0.0), (110.0, 0.38, 1.0, 0.0), (110, 0.38, 0.0, 1.0, ),(110, 0.38, 1.0, 1.0)))
        mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1',material='MATRIX',thickness=1.0)  #定义截面1
        
        mdb.models['Model-1'].Material(name='FIBER')   #定义材料名称2
        mdb.models['Model-1'].materials['FIBER'].Elastic(dependencies=2, table=((220000, 
            0.25, 0.0, 0.0), (22000, 0.25, 1.0, 0.0), (22000, 0.25, 0.0, 1.0, ),(22000, 0.25, 1.0, 1.0)))
        mdb.models['Model-1'].HomogeneousSolidSection(name='Section-2',material='FIBER',thickness=1.0)  #定义截面2
        
        faces = mdb.models['Model-1'].parts['Part-1'].faces.findAt(((0.0, 0.0, 0.0), ))
        region =(faces, )     #以上两行找到包含点（0,0,0）的面，保存到region 
        mdb.models['Model-1'].parts['Part-1'].SectionAssignment(region=region, sectionName='Section-1') #截面属性附给选中的面region 
        
        f2=mdb.models['Model-1'].parts['Part-1'].faces
        for i in range(len(fiber_vertices)+1):
            if f2[i:i+1]==faces:
                j=i
        
        faces2=f2[0:j]+f2[j+1:len(fiber_vertices)+1]
        region2 =(faces2, )     #以上找到除faces以外的面，保存到region2 
        mdb.models['Model-1'].parts['Part-1'].SectionAssignment(region=region2, sectionName='Section-2') #截面属性2附给选中的面region2 
        
        from assembly import *     #第三步，装配
        a1 = mdb.models['Model-1'].rootAssembly
        p = mdb.models['Model-1'].parts['Part-1']  #指定part-1
        a1.Instance(name='Part-1-1', part=p, dependent=OFF) #生成part-1对象的实体Part-1-1，independent网格在Instance上面
        
        from mesh import *  #第五步, 网格划分控制
        elemType1 = mesh.ElemType(elemCode=CPS4R, elemLibrary=STANDARD)
        elemType2 = mesh.ElemType(elemCode=CPS3, elemLibrary=STANDARD)
        faces = mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces
        pickedRegions =(faces, )
        mdb.models['Model-1'].rootAssembly.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))   #定义两种网格类型
        
        #size0=float(getInput("Input the mesh size:","0.01"))
        pickedEdges=a1.instances['Part-1-1'].edges
        a1.seedEdgeBySize(edges=pickedEdges, size=size0,constraint=FIXED) #撒网格种子
        partInstances =(a1.instances['Part-1-1'], )
        a1.generateMesh(regions=partInstances) #给partInstances划分网格
        
        from interaction import *   #第六步, 定义多点约束条件-----MPC
        m=mdb.models['Model-1']
        r=m.rootAssembly
        node=r.instances['Part-1-1'].nodes
        ne=[]    #ne 存储所有边界上的单元节点的编号
        for i in range(len(node)):
            x=node[i].coordinates[0]
            y=node[i].coordinates[1]
            flag=(x-bwidx)*(x-0)*(y-bwidy)*(y-0)
            if abs(flag)<0.00000000001:
                ne.append(i)
        print "ne0=", len(ne)
        for i in range(len(ne)):     #找出四个顶点
            x=node[ne[i]].coordinates[0]
            y=node[ne[i]].coordinates[1]
            if (abs(x-0)<0.000001)and(abs(y-0)<0.000001):
                r.Set(nodes=node[ne[i]:ne[i]+1],name='set-01')
                aa1=i
            elif(abs(x-bwidx)<0.000001)and(abs(y-0)<0.000001):
                r.Set(nodes=node[ne[i]:ne[i]+1],name='set-02')
                aa2=i
            elif(abs(x-0)<0.000001)and(abs(y-bwidy)<0.000001):
                r.Set(nodes=node[ne[i]:ne[i]+1],name='set-03')
                aa3=i
            elif(abs(x-bwidx)<0.000001)and(abs(y-bwidy)<0.000001):
                r.Set(nodes=node[ne[i]:ne[i]+1],name='set-04')
                aa4=i
        
        aa=[aa1,aa2,aa3,aa4]
        aa.sort()
        del ne[aa[3]];del ne[aa[2]];del ne[aa[1]];del ne[aa[0]]
        #print a1,a2,a3,a4
        print "ne1=", len(ne)
        m.Equation(name='eq-00',terms=((1,'set-02',1),(-1,'set-04',1),(1,'set-03',1))) #定义角点的MPC
        m.Equation(name='eq-01',terms=((1,'set-03',2),(-1,'set-04',2),(1,'set-02',2)))
        
        from step import *  #第四步, 定义分析步
        mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial',
            timeIncrementationMethod=FIXED, initialInc=1, noStop=OFF)  #定义一个固定增量的静态分析步
        regionDef=mdb.models['Model-1'].rootAssembly.sets['set-04']
        mdb.models['Model-1'].StaticRiksStep(name='Step-1', previous='Initial',    #定义弧长法分析步
            nodeOn=ON, maximumDisplacement=0.1, region=regionDef, dof=1, 
            maxNumInc=10000, initialArcInc=0.0001, minArcInc=0.00001, maxArcInc=100000, 
            nlgeom=ON)
        mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValuesInStep(stepName='Step-1',
            variables=('S', 'U', 'COORD'))  #定义输出到ODB文件的数据(应力、位移)
        #-----------------------------定义其他边界点的MPC----------------
        i=0
        for n in range(len(ne)):
            print n
            x0=node[ne[n]].coordinates[0]
            y0=node[ne[n]].coordinates[1]
            for j in range(n+1,len(ne)):
                x1=node[ne[j]].coordinates[0]
                y1=node[ne[j]].coordinates[1]
                if (abs(x0-x1)<0.00001)and(abs(abs(y0-y1)-L)<0.00001)or(abs(y0-y1)<0.00001)and(abs(abs(x0-x1)-L)<0.00001):
                    r.Set(nodes=node[ne[n]:ne[n]+1],name='set'+str(2*i+1))  ##定义边界上对应两个节点
                    r.Set(nodes=node[ne[j]:ne[j]+1],name='set'+str(2*i+2))
                    if abs(y0-L)<0.00001:    #0节点在上，1节点在下
                        m.Equation(name='eq'+str(2*i+1),terms=((1,'set'+str(2*i+1),1),(-1,'set-03',1),(-1,'set'+str(2*i+2),1)))
                        m.Equation(name='eq'+str(2*i+2),terms=((1,'set'+str(2*i+1),2),(-1,'set-03',2),(-1,'set'+str(2*i+2),2)))
                    elif abs(y1-L)<0.00001:   #1节点在上，0节点在下
                        m.Equation(name='eq'+str(2*i+1),terms=((1,'set'+str(2*i+2),1),(-1,'set-03',1),(-1,'set'+str(2*i+1),1)))
                        m.Equation(name='eq'+str(2*i+2),terms=((1,'set'+str(2*i+2),2),(-1,'set-03',2),(-1,'set'+str(2*i+1),2)))
                    elif abs(x0-L)<0.00001:   #0节点在右，1节点在左
                        m.Equation(name='eq'+str(2*i+1),terms=((1,'set'+str(2*i+1),1),(-1,'set-04',1),(-1,'set'+str(2*i+2),1)))
                        m.Equation(name='eq'+str(2*i+2),terms=((1,'set'+str(2*i+1),2),(-1,'set-02',2),(-1,'set'+str(2*i+2),2)))
                    elif abs(x1-L)<0.00001:   #1节点在右，0节点在左
                        m.Equation(name='eq'+str(2*i+1),terms=((1,'set'+str(2*i+2),1),(-1,'set-04',1),(-1,'set'+str(2*i+1),1)))
                        m.Equation(name='eq'+str(2*i+2),terms=((1,'set'+str(2*i+2),2),(-1,'set-02',2),(-1,'set'+str(2*i+1),2)))
                    i=i+1
                    break
        print "i=",i    
        #--------------------------------------------------------------    
        from load import *   #第七步, 荷载边界定义
        m=mdb.models['Model-1']                  
        region = m.rootAssembly.sets['set-01']    #选中固支节点，保存到region
        m.DisplacementBC(name='BC-1', createStepName='Initial',region=region,
            u1=SET, u2=SET, amplitude=UNSET,distributionType=UNIFORM, localCsys=None) #定义固支边界
        
        region = m.rootAssembly.sets['set-02']    #选中简支节点，保存到region
        m.DisplacementBC(name='BC-2', createStepName='Initial',region=region,
            u1=UNSET, u2=SET, amplitude=UNSET,distributionType=UNIFORM, localCsys=None) #定义简支边界
        
        region = m.rootAssembly.sets['set-03']    #选中加载节点，保存到region
        m.DisplacementBC(name='BC-3', createStepName='Initial',region=region,
            u1=SET, u2=UNSET, amplitude=UNSET, distributionType=UNIFORM, localCsys=None) #定义简支边界
        
        region = m.rootAssembly.sets['set-04']    #选中加载节点，保存到region
        m.DisplacementBC(name='BC-4', createStepName='Step-1',region=region,
            u1=0.06, u2=UNSET, amplitude=UNSET, fixed=OFF,distributionType=UNIFORM, localCsys=None) #定义位移载荷
        
        ####### 提交作业
        #job_name=getInput('Job name:','name')
        mdb.Job(name=job_name, model='Model-1', description='', type=ANALYSIS, 
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, 
            scratch='', multiprocessingMode=DEFAULT, numCpus=1)
        mdb.saveAs(Pathname+'\\'+job_name)
        mdb.jobs[job_name].submit(consistencyChecking=OFF)
        mdb.jobs[job_name].waitForCompletion()
#-----------------------------------------第十步，后处理
        o1 = session.openOdb(job_name+'.odb')
        coorList = o1.steps['Step-1'].frames[0].fieldOutputs['COORD'].values
        for i in range(len(coorList)):
            x = coorList[i].data[0]
            y = coorList[i].data[1]
            if abs(x-bwidx) < 0.5*size0 and abs(y) < 0.5*size0:
                rd = i+1
                break       #检测(bwidx,0)处的Node编号
        
        for i in range(len(coorList)):
            x = coorList[i].data[0]
            y = coorList[i].data[1]
            if abs(x) < 0.5*size0 and abs(y-bwidy) < 0.5*size0:
                lu = i+1
                break       #检测(bwidx,0)处的Node编号
        
        nodeName_rd = 'Node PART-1-1.'+str(rd)
        nodeName_lu = 'Node PART-1-1.'+str(lu)
        RF1 = o1.steps['Step-1'].historyRegions[nodeName_rd].historyOutputs['RF1'].data[1][1]
        U1 = o1.steps['Step-1'].historyRegions[nodeName_rd].historyOutputs['U1'].data[1][1]
        RF2 = o1.steps['Step-1'].historyRegions[nodeName_lu].historyOutputs['RF2'].data[1][1]
        U2 = o1.steps['Step-1'].historyRegions[nodeName_lu].historyOutputs['U2'].data[1][1]
        ffo.write(job_name+'\t')
        ffo.write('%.3F\t%.3F\t%.3F\t%.3F\n' % (RF1,U1,RF2,U2))
    except:
        print ('Wrong')
    Mdb()

ffo.close()
f.close()

