# -*- coding: cp936 -*-
#filename:abaqus_1.py

####################################定义函数
#####
#####点和向量点乘
def doc(vertice,edge):
    axis=[edge[0]/sqrt(edge[0]**2+edge[1]**2),edge[1]/sqrt(edge[0]**2+edge[1]**2)]
    doc=vertice[0]*edge[0]+vertice[1]*edge[1]
    return doc

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
    dis = abs((vertice[1]-k*vertice[0]-b)/sqrt(k**2+1))
    return dis

#####
#####两根纤维是否发生交叉
def oveDownLap(fiber1,fiber2):
    vertices1=[[]]
    vertices2=[[]]
    edge=[[]]
    del vertices1[0]
    del vertices2[0]
    del edge[0]
    for i in range(4):  #####找出两个矩形八个顶点
        vertices1.append([fiber1[1+2*i],fiber1[2+2*i]])
    for i in range(4):
        vertices2.append([fiber2[1+2*i],fiber2[2+2*i]])
    for i in range(2): ######找出两个矩形四条投影边
        edge.append([vertices1[i+1][0]-vertices1[i][0],vertices1[i+1][1]-vertices1[i][1]])
    for i in range(2):
        edge.append([vertices2[i+1][0]-vertices2[i][0],vertices2[i+1][1]-vertices2[i][1]])
    
    non_cross=[]
    count = 0
    for i in range(4):
        docs=[]
        for j in range(4):
            docs.append(doc(vertices1[j],edge[i]))
        max1=max(docs)
        min1=min(docs)
        del docs
        docs=[]
        for j in range(4):
            docs.append(doc(vertices2[j],edge[i]))
        max2=max(docs)
        min2=min(docs)
        del docs
        if max2<(min1-0) or min2>(max1+0):
            non_cross.append(1)
            count += 1
            break
        else:
            non_cross.append(0)
    if max(non_cross)==1:
        cross.append(0)
    else:
        return(1)
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
    dis1=[disl([x_ShortL1,y_ShortL1],vertices2[0],vertices2[1]),disl([x_ShortL1,y_ShortL1],vertices2[1],vertices2[2]),disl([x_ShortL1,y_ShortL1],vertices2[2],vertices2[3]),disl([x_ShortL1,y_ShortL1],vertices2[0],vertices2[3]),disl([x_ShortR1,y_ShortR1],vertices2[0],vertices2[1]),disl([x_ShortR1,y_ShortR1],vertices2[1],vertices2[2]),disl([x_ShortR1,y_ShortR1],vertices2[2],vertices2[3]),disl([x_ShortR1,y_ShortR1],vertices2[0],vertices2[3])]
    dis2=[disl([x_ShortL2,y_ShortL2],vertices1[0],vertices1[1]),disl([x_ShortL2,y_ShortL2],vertices1[1],vertices1[2]),disl([x_ShortL2,y_ShortL2],vertices1[2],vertices1[3]),disl([x_ShortL2,y_ShortL2],vertices1[0],vertices1[3]),disl([x_ShortR2,y_ShortR2],vertices1[0],vertices1[1]),disl([x_ShortR2,y_ShortR2],vertices1[1],vertices1[2]),disl([x_ShortR2,y_ShortR2],vertices1[2],vertices1[3]),disl([x_ShortR2,y_ShortR2],vertices1[0],vertices1[3])]
    
    if min(disd([x_ShortL1,y_ShortL1],[x_ShortL2,y_ShortL2]),disd([x_ShortL1,y_ShortL1],[x_ShortR2,y_ShortR2]),disd([x_ShortR1,y_ShortR1],[x_ShortL2,y_ShortL2]),disd([x_ShortR1,y_ShortR1],[x_ShortR2,y_ShortR2])) < 2*c_rad:
        return 1
    if (x_ShortL1 > x_ShortL2 and x_ShortL1 < x_ShortR2) or (x_ShortR1 > x_ShortL2 and x_ShortR1 < x_ShortR2):
        if min(dis1) < c_rad or min(dis2) < c_rad:
            return 1
    return 0

f=open('D:\\PythonCode\\bishe\\bones.txt','r')
i=0
for line in f:
    i=i+1
    print i
    data=line.split()
    bwidx=float(data[0])#基体宽度
    bwidy=float(data[1])#基体长度
    f_len=float(data[2])#纤维长度
    f_wid=float(data[3])#纤维宽度
    f_dis=float(data[4])#纤维最小间距一半
    c_rad=float(data[5])#圆头半径
    r_rad=float(data[6])#圆角半径
    f_num=int(data[7])  #纤维数目
    size0=float(data[8])#网格尺寸
    job_name=data[9]    #工作名称
    Pathname=data[10]
    
    ####################################调用模块
    from random import *
    from abaqus import *
    from abaqusConstants import *
    from caeModules import *
    from driverUtils import executeOnCaeStartup
    from abaqus import backwardCompatibility
    backwardCompatibility.setValues(reportDeprecated=False)
    import os
    os.chdir(Pathname)
    executeOnCaeStartup()
    
    Mdb()
    #纤维生成
    from math import *
    L=bwidx   #基体长度
    B=bwidy   #基体宽度 
    f_num_new=0   #计入被边界截断的纤维数目
    f_len_temp=f_len+f_dis#较粗大纤维长度，用以确保纤维之间距离不能太小
    f_wid_temp=f_wid+f_dis#较粗大纤维宽度，用以确保纤维之间距离不能太小
    fiber_vertices=[[]]   #创建矩阵存储纤维编号和四个顶点坐标
    fiber_vertices_temp=[[]]  #创建临时矩阵存储较宽的纤维编号和四个顶点坐标，用以确保纤维之间距离不能太小
    del fiber_vertices[0]
    del fiber_vertices_temp[0]
    #####
    #####纤维生成
    
    for i in range(1,f_num+1):
        print(i)
        do=0   #判断纤维是否生成成功
        while do==0:
            x_m=L*random()
            y_m=L*random()
            angle=pi*gauss(0,23.4)/180
            #angle=pi*(random()-0.5)
            cl=sqrt(f_len**2+f_wid**2)
            cm=sqrt(f_len_temp**2+f_wid_temp**2)
            x_L=x_m-f_len/2*cos(angle)
            y_L=y_m-f_len/2*sin(angle)
            x_R=x_m+f_len/2*cos(angle)
            y_R=y_m+f_len/2*sin(angle)
            x_L_temp=x_m-f_len_temp/2*cos(angle)
            y_L_temp=y_m-f_len_temp/2*sin(angle)
            x_R_temp=x_m+f_len_temp/2*cos(angle)
            y_R_temp=y_m+f_len_temp/2*sin(angle)
            if angle==0 or angle==pi/2 or angle==-pi/2 or angle==pi/4 or angle==-pi/4:
                continue
            else:
                k_=tan(angle)
                
                x_UpR=x_m-(k_*k_*f_wid/abs(sin(angle))-f_len/abs(cos(angle)))/2/(k_*k_+1)
                y_UpR=y_m+k_*(f_len/abs(cos(angle))+f_wid/abs(sin(angle)))/2/(k_*k_+1)
                x_UpL=x_m-(k_*k_*f_wid/abs(sin(angle))+f_len/abs(cos(angle)))/2/(k_*k_+1)
                y_UpL=y_m-k_*(f_len/abs(cos(angle))-f_wid/abs(sin(angle)))/2/(k_*k_+1)
                x_DownR=x_m+(k_*k_*f_wid/abs(sin(angle))+f_len/abs(cos(angle)))/2/(k_*k_+1)
                y_DownR=y_m+k_*(f_len/abs(cos(angle))-f_wid/abs(sin(angle)))/2/(k_*k_+1)
                x_DownL=x_m+(k_*k_*f_wid/abs(sin(angle))-f_len/abs(cos(angle)))/2/(k_*k_+1)
                y_DownL=y_m-k_*(f_len/abs(cos(angle))+f_wid/abs(sin(angle)))/2/(k_*k_+1)
                x_UpR_temp=x_m-(k_*k_*f_wid_temp/abs(sin(angle))-f_len_temp/abs(cos(angle)))/2/(k_*k_+1)
                y_UpR_temp=y_m+k_*(f_len_temp/abs(cos(angle))+f_wid_temp/abs(sin(angle)))/2/(k_*k_+1)
                x_UpL_temp=x_m-(k_*k_*f_wid_temp/abs(sin(angle))+f_len_temp/abs(cos(angle)))/2/(k_*k_+1)
                y_UpL_temp=y_m-k_*(f_len_temp/abs(cos(angle))-f_wid_temp/abs(sin(angle)))/2/(k_*k_+1)
                x_DownR_temp=x_m+(k_*k_*f_wid_temp/abs(sin(angle))+f_len_temp/abs(cos(angle)))/2/(k_*k_+1)
                y_DownR_temp=y_m+k_*(f_len_temp/abs(cos(angle))-f_wid_temp/abs(sin(angle)))/2/(k_*k_+1)
                x_DownL_temp=x_m+(k_*k_*f_wid_temp/abs(sin(angle))-f_len_temp/abs(cos(angle)))/2/(k_*k_+1)
                y_DownL_temp=y_m-k_*(f_len_temp/abs(cos(angle))+f_wid_temp/abs(sin(angle)))/2/(k_*k_+1)
                
                R=c_rad
                if abs(disd([x_UpL,y_UpL],[x_DownL,y_DownL])-f_wid)<0.5*f_wid:
                    x_LC=(x_UpL+x_DownL)/2
                    y_LC=(y_UpL+y_DownL)/2
                    x_RC=(x_UpR+x_DownR)/2
                    y_RC=(y_UpR+y_DownR)/2
                elif abs(disd([x_UpL,y_UpL],[x_DownR,y_DownR])-f_wid)<0.5*f_wid:
                    x_LC=(x_UpL+x_DownR)/2
                    y_LC=(y_UpL+y_DownR)/2
                    x_RC=(x_UpR+x_DownL)/2
                    y_RC=(y_UpR+y_DownL)/2
                elif abs(disd([x_UpL,y_UpL],[x_UpR,y_UpR])-f_wid)<0.5*f_wid:
                    x_LC=(x_UpL+x_UpR)/2
                    y_LC=(y_UpL+y_UpR)/2
                    x_RC=(x_DownR+x_DownL)/2
                    y_RC=(y_DownR+y_DownL)/2
                if (min(x_UpL,x_DownL)<=0 and min(y_UpL,y_DownL,y_UpR,y_DownR)<=0) or (x_LC<=R and min(y_LC,y_RC)<=R):
                    continue
                elif (min(x_UpL,x_DownL)<=0 and max(y_UpL,y_DownL,y_UpR,y_DownR)>=L) or (x_LC<=R and max(y_LC,y_RC)>=L-R):
                    continue
                elif (max(x_DownR,x_UpR)-L>=0 and min(y_UpL,y_DownL,y_UpR,y_DownR)<=0) or (x_RC>=L-R and min(y_LC,y_RC)<=R):
                    continue
                elif (max(x_DownR,x_UpR)-L>=0 and max(y_UpL,y_DownL,y_UpR,y_DownR)>=L) or (x_RC>=L-R and max(y_LC,y_RC)>=L-R):
                    continue
                elif min(x_UpL,x_DownL)>=0 and max(x_UpR,x_DownR)<=L and min(y_UpL,y_DownL,y_UpR,y_DownR)>=0 and max(y_UpL,y_DownL,y_UpR,y_DownR)<=L and x_LC>=R and x_RC<=L-R and min(y_LC,y_RC)>=R and max(y_LC,y_RC)<=L-R:#纤维与边界无交点       
                    if k_>0: 
                        cross=[]
                        if len(fiber_vertices)==0:
                            fiber_vertices.append([i,x_UpL,y_UpL,x_DownL,y_DownL,x_DownR,y_DownR,x_UpR,y_UpR])
                            fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp,x_DownL_temp,y_DownL_temp,x_DownR_temp,y_DownR_temp,x_UpR_temp,y_UpR_temp])
                            break
                        else:
                            temp=[i,x_UpL_temp,y_UpL_temp,x_DownL_temp,y_DownL_temp,x_DownR_temp,y_DownR_temp,x_UpR_temp,y_UpR_temp]
                            for j in range(len(fiber_vertices_temp)):
                                cross.append(oveDownLap(fiber_vertices_temp[j],temp))
                            if max(cross)==1:
                                del cross
                                continue
                            else:
                                fiber_vertices.append([i,x_UpL,y_UpL,x_DownL,y_DownL,x_DownR,y_DownR,x_UpR,y_UpR])
                                fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp,x_DownL_temp,y_DownL_temp,x_DownR_temp,y_DownR_temp,x_UpR_temp,y_UpR_temp])
                                del cross
                                break
                    else:
                        cross=[]
                        if len(fiber_vertices)==0:
                            fiber_vertices.append([i,x_UpL,y_UpL,x_UpR,y_UpR,x_DownR,y_DownR,x_DownL,y_DownL])
                            fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp,x_UpR_temp,y_UpR_temp,x_DownR_temp,y_DownR_temp,x_DownL_temp,y_DownL_temp])
                            break
                        else:
                            temp=[i,x_UpL_temp,y_UpL_temp,x_UpR_temp,y_UpR_temp,x_DownR_temp,y_DownR_temp,x_DownL_temp,y_DownL_temp]
                            for j in range(len(fiber_vertices_temp)):
                                cross.append(oveDownLap(fiber_vertices_temp[j],temp))
                            if max(cross)==1:
                                del cross
                                continue
                            else:
                                fiber_vertices.append([i,x_UpL,y_UpL,x_UpR,y_UpR,x_DownR,y_DownR,x_DownL,y_DownL])
                                fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp,x_UpR_temp,y_UpR_temp,x_DownR_temp,y_DownR_temp,x_DownL_temp,y_DownL_temp])
                                del cross
                                break                
                elif x_LC-R<0 and min(x_UpR,x_DownR)>0:#纤维与左边界有交点
                    if k_>0:
                        cross=[]                 
                        if len(fiber_vertices)==0:
                            fiber_vertices.append([i,x_UpL,y_UpL,x_DownL,y_DownL,x_DownR,y_DownR,x_UpR,y_UpR])
                            fiber_vertices.append([i,x_UpL+L,y_UpL,x_DownL+L,y_DownL,x_DownR+L,y_DownR,x_UpR+L,y_UpR])
                            fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp,x_DownL_temp,y_DownL_temp,x_DownR_temp,y_DownR_temp,x_UpR_temp,y_UpR_temp])
                            fiber_vertices_temp.append([i,x_UpL_temp+L,y_UpL_temp,x_DownL_temp+L,y_DownL_temp,x_DownR_temp+L,y_DownR_temp,x_UpR_temp+L,y_UpR_temp])                    
                            break
                        else:
                            temp1=[i,x_UpL_temp,y_UpL_temp,x_DownL_temp,y_DownL_temp,x_DownR_temp,y_DownR_temp,x_UpR_temp,y_UpR_temp]
                            for j in range(len(fiber_vertices_temp)):
                                cross.append(oveDownLap(fiber_vertices_temp[j],temp1))
                            temp2=[i,x_UpL_temp+L,y_UpL_temp,x_DownL_temp+L,y_DownL_temp,x_DownR_temp+L,y_DownR_temp,x_UpR_temp+L,y_UpR_temp]
                            for j in range(len(fiber_vertices_temp)):
                                cross.append(oveDownLap(fiber_vertices_temp[j],temp2))                    
                            if max(cross)==1:
                                del cross
                                continue
                            else:
                                fiber_vertices.append([i,x_UpL,y_UpL,x_DownL,y_DownL,x_DownR,y_DownR,x_UpR,y_UpR])
                                fiber_vertices.append([i,x_UpL+L,y_UpL,x_DownL+L,y_DownL,x_DownR+L,y_DownR,x_UpR+L,y_UpR])
                                fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp,x_DownL_temp,y_DownL_temp,x_DownR_temp,y_DownR_temp,x_UpR_temp,y_UpR_temp])
                                fiber_vertices_temp.append([i,x_UpL_temp+L,y_UpL_temp,x_DownL_temp+L,y_DownL_temp,x_DownR_temp+L,y_DownR_temp,x_UpR_temp+L,y_UpR_temp])                             
                                del cross
                                break
                    else:
                        cross=[]                
                        if len(fiber_vertices)==0:
                            fiber_vertices.append([i,x_UpL,y_UpL,x_UpR,y_UpR,x_DownR,y_DownR,x_DownL,y_DownL])
                            fiber_vertices.append([i,x_UpL+L,y_UpL,x_UpR+L,y_UpR,x_DownR+L,y_DownR,x_DownL+L,y_DownL])
                            fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp,x_UpR_temp,y_UpR_temp,x_DownR_temp,y_DownR_temp,x_DownL_temp,y_DownL_temp])
                            fiber_vertices_temp.append([i,x_UpL_temp+L,y_UpL_temp,x_UpR_temp+L,y_UpR_temp,x_DownR_temp+L,y_DownR_temp,x_DownL_temp+L,y_DownL_temp])                    
                            break
                        else:
                            temp1=[i,x_UpL_temp,y_UpL_temp,x_UpR_temp,y_UpR_temp,x_DownR_temp,y_DownR_temp,x_DownL_temp,y_DownL_temp]
                            for j in range(len(fiber_vertices_temp)):
                                cross.append(oveDownLap(fiber_vertices_temp[j],temp1))
                            temp2=[i,x_UpL_temp+L,y_UpL_temp,x_UpR_temp+L,y_UpR_temp,x_DownR_temp+L,y_DownR_temp,x_DownL_temp+L,y_DownL_temp]
                            for j in range(len(fiber_vertices_temp)):
                                cross.append(oveDownLap(fiber_vertices_temp[j],temp2))                    
                            if max(cross)==1:
                                del cross
                                continue
                            else:
                                fiber_vertices.append([i,x_UpL,y_UpL,x_UpR,y_UpR,x_DownR,y_DownR,x_DownL,y_DownL])
                                fiber_vertices.append([i,x_UpL+L,y_UpL,x_UpR+L,y_UpR,x_DownR+L,y_DownR,x_DownL+L,y_DownL])
                                fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp,x_UpR_temp,y_UpR_temp,x_DownR_temp,y_DownR_temp,x_DownL_temp,y_DownL_temp])
                                fiber_vertices_temp.append([i,x_UpL_temp+L,y_UpL_temp,x_UpR_temp+L,y_UpR_temp,x_DownR_temp+L,y_DownR_temp,x_DownL_temp+L,y_DownL_temp])                         
                                del cross
                                break                                                          
                elif max(x_UpL,x_DownL)<L and max(x_LC,x_RC)+R>L:#纤维与右边界有交点
                    if k_>0:
                        cross=[]
                        if len(fiber_vertices)==0:
                            fiber_vertices.append([i,x_UpL,y_UpL,x_DownL,y_DownL,x_DownR,y_DownR,x_UpR,y_UpR])
                            fiber_vertices.append([i,x_UpL-L,y_UpL,x_DownL-L,y_DownL,x_DownR-L,y_DownR,x_UpR-L,y_UpR])
                            fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp,x_DownL_temp,y_DownL_temp,x_DownR_temp,y_DownR_temp,x_UpR_temp,y_UpR_temp])
                            fiber_vertices_temp.append([i,x_UpL_temp-L,y_UpL_temp,x_DownL_temp-L,y_DownL_temp,x_DownR_temp-L,y_DownR_temp,x_UpR_temp-L,y_UpR_temp])                    
                            break
                        else:
                            temp1=[i,x_UpL_temp,y_UpL_temp,x_DownL_temp,y_DownL_temp,x_DownR_temp,y_DownR_temp,x_UpR_temp,y_UpR_temp]
                            for j in range(len(fiber_vertices_temp)):
                                cross.append(oveDownLap(fiber_vertices_temp[j],temp1))
                            temp2=[i,x_UpL_temp-L,y_UpL_temp,x_DownL_temp-L,y_DownL_temp,x_DownR_temp-L,y_DownR_temp,x_UpR_temp-L,y_UpR_temp]
                            for j in range(len(fiber_vertices_temp)):
                                cross.append(oveDownLap(fiber_vertices_temp[j],temp2))                    
                            if max(cross)==1:
                                del cross
                                continue
                            else:
                                fiber_vertices.append([i,x_UpL,y_UpL,x_DownL,y_DownL,x_DownR,y_DownR,x_UpR,y_UpR])
                                fiber_vertices.append([i,x_UpL-L,y_UpL,x_DownL-L,y_DownL,x_DownR-L,y_DownR,x_UpR-L,y_UpR])
                                fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp,x_DownL_temp,y_DownL_temp,x_DownR_temp,y_DownR_temp,x_UpR_temp,y_UpR_temp])
                                fiber_vertices_temp.append([i,x_UpL_temp-L,y_UpL_temp,x_DownL_temp-L,y_DownL_temp,x_DownR_temp-L,y_DownR_temp,x_UpR_temp-L,y_UpR_temp])                           
                                del cross
                                break
                    else:
                        cross=[]
                        if len(fiber_vertices)==0:
                            fiber_vertices.append([i,x_UpL,y_UpL,x_UpR,y_UpR,x_DownR,y_DownR,x_DownL,y_DownL])
                            fiber_vertices.append([i,x_UpL-L,y_UpL,x_UpR-L,y_UpR,x_DownR-L,y_DownR,x_DownL-L,y_DownL])
                            fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp,x_UpR_temp,y_UpR_temp,x_DownR_temp,y_DownR_temp,x_DownL_temp,y_DownL_temp])
                            fiber_vertices_temp.append([i,x_UpL_temp-L,y_UpL_temp,x_UpR_temp-L,y_UpR_temp,x_DownR_temp-L,y_DownR_temp,x_DownL_temp-L,y_DownL_temp])                           
                            break
                        else:
                            temp1=[i,x_UpL_temp,y_UpL_temp,x_UpR_temp,y_UpR_temp,x_DownR_temp,y_DownR_temp,x_DownL_temp,y_DownL_temp]
                            for j in range(len(fiber_vertices_temp)):
                                cross.append(oveDownLap(fiber_vertices_temp[j],temp1))
                            temp2=[i,x_UpL_temp-L,y_UpL_temp,x_UpR_temp-L,y_UpR_temp,x_DownR_temp-L,y_DownR_temp,x_DownL_temp-L,y_DownL_temp]
                            for j in range(len(fiber_vertices_temp)):
                                cross.append(oveDownLap(fiber_vertices_temp[j],temp2))                    
                            if max(cross)==1:
                                del cross
                                continue
                            else:
                                fiber_vertices.append([i,x_UpL,y_UpL,x_UpR,y_UpR,x_DownR,y_DownR,x_DownL,y_DownL])
                                fiber_vertices.append([i,x_UpL-L,y_UpL,x_UpR-L,y_UpR,x_DownR-L,y_DownR,x_DownL-L,y_DownL])
                                fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp,x_UpR_temp,y_UpR_temp,x_DownR_temp,y_DownR_temp,x_DownL_temp,y_DownL_temp])
                                fiber_vertices_temp.append([i,x_UpL_temp-L,y_UpL_temp,x_UpR_temp-L,y_UpR_temp,x_DownR_temp-L,y_DownR_temp,x_DownL_temp-L,y_DownL_temp])                             
                                del cross
                                break                           
                elif max(y_LC+R,y_RC+R)>L:#纤维与上边界有交点
                    if k_>0:
                        cross=[]
                        if len(fiber_vertices)==0:
                            fiber_vertices.append([i,x_UpL,y_UpL,x_DownL,y_DownL,x_DownR,y_DownR,x_UpR,y_UpR])
                            fiber_vertices.append([i,x_UpL,y_UpL-L,x_DownL,y_DownL-L,x_DownR,y_DownR-L,x_UpR,y_UpR-L])
                            fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp,x_DownL_temp,y_DownL_temp,x_DownR_temp,y_DownR_temp,x_UpR_temp,y_UpR_temp])
                            fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp-L,x_DownL_temp,y_DownL_temp-L,x_DownR_temp,y_DownR_temp-L,x_UpR_temp,y_UpR_temp-L])                           
                            break
                        else:
                            temp1=[i,x_UpL_temp,y_UpL_temp,x_DownL_temp,y_DownL_temp,x_DownR_temp,y_DownR_temp,x_UpR_temp,y_UpR_temp]
                            for j in range(len(fiber_vertices_temp)):
                                cross.append(oveDownLap(fiber_vertices_temp[j],temp1))
                            temp2=[i,x_UpL_temp,y_UpL_temp-L,x_DownL_temp,y_DownL_temp-L,x_DownR_temp,y_DownR_temp-L,x_UpR_temp,y_UpR_temp-L]
                            for j in range(len(fiber_vertices_temp)):
                                cross.append(oveDownLap(fiber_vertices_temp[j],temp2))                    
                            if max(cross)==1:
                                del cross
                                continue
                            else:
                                fiber_vertices.append([i,x_UpL,y_UpL,x_DownL,y_DownL,x_DownR,y_DownR,x_UpR,y_UpR])
                                fiber_vertices.append([i,x_UpL,y_UpL-L,x_DownL,y_DownL-L,x_DownR,y_DownR-L,x_UpR,y_UpR-L])
                                fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp,x_DownL_temp,y_DownL_temp,x_DownR_temp,y_DownR_temp,x_UpR_temp,y_UpR_temp])
                                fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp-L,x_DownL_temp,y_DownL_temp-L,x_DownR_temp,y_DownR_temp-L,x_UpR_temp,y_UpR_temp-L])                            
                                del cross
                                break
                    else:
                        cross=[]
                        if len(fiber_vertices)==0:
                            fiber_vertices.append([i,x_UpL,y_UpL,x_UpR,y_UpR,x_DownR,y_DownR,x_DownL,y_DownL])
                            fiber_vertices.append([i,x_UpL,y_UpL-L,x_UpR,y_UpR-L,x_DownR,y_DownR-L,x_DownL,y_DownL-L])
                            fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp,x_UpR_temp,y_UpR_temp,x_DownR_temp,y_DownR_temp,x_DownL_temp,y_DownL_temp])
                            fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp-L,x_UpR_temp,y_UpR_temp-L,x_DownR_temp,y_DownR_temp-L,x_DownL_temp,y_DownL_temp-L])                           
                            break
                        else:
                            temp1=[i,x_UpL_temp,y_UpL_temp,x_UpR_temp,y_UpR_temp,x_DownR_temp,y_DownR_temp,x_DownL_temp,y_DownL_temp]
                            for j in range(len(fiber_vertices_temp)):
                                cross.append(oveDownLap(fiber_vertices_temp[j],temp1))
                            temp2=[i,x_UpL_temp,y_UpL_temp-L,x_UpR_temp,y_UpR_temp-L,x_DownR_temp,y_DownR_temp-L,x_DownL_temp,y_DownL_temp-L]
                            for j in range(len(fiber_vertices_temp)):
                                cross.append(oveDownLap(fiber_vertices_temp[j],temp2))                    
                            if max(cross)==1:
                                del cross
                                continue
                            else:
                                fiber_vertices.append([i,x_UpL,y_UpL,x_UpR,y_UpR,x_DownR,y_DownR,x_DownL,y_DownL])
                                fiber_vertices.append([i,x_UpL,y_UpL-L,x_UpR,y_UpR-L,x_DownR,y_DownR-L,x_DownL,y_DownL-L])
                                fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp,x_UpR_temp,y_UpR_temp,x_DownR_temp,y_DownR_temp,x_DownL_temp,y_DownL_temp])
                                fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp-L,x_UpR_temp,y_UpR_temp-L,x_DownR_temp,y_DownR_temp-L,x_DownL_temp,y_DownL_temp-L])                             
                                del cross
                                break                
                elif min(y_LC-R,y_RC-R)<0:#纤维与下边界有交点
                    if k_>0:
                        cross=[]
                        if len(fiber_vertices)==0:
                            fiber_vertices.append([i,x_UpL,y_UpL,x_DownL,y_DownL,x_DownR,y_DownR,x_UpR,y_UpR])
                            fiber_vertices.append([i,x_UpL,y_UpL+L,x_DownL,y_DownL+L,x_DownR,y_DownR+L,x_UpR,y_UpR+L])
                            fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp,x_DownL_temp,y_DownL_temp,x_DownR_temp,y_DownR_temp,x_UpR_temp,y_UpR_temp])
                            fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp+L,x_DownL_temp,y_DownL_temp+L,x_DownR_temp,y_DownR_temp+L,x_UpR_temp,y_UpR_temp+L])                           
                            break
                        else:
                            temp1=[i,x_UpL_temp,y_UpL_temp,x_DownL_temp,y_DownL_temp,x_DownR_temp,y_DownR_temp,x_UpR_temp,y_UpR_temp]
                            for j in range(len(fiber_vertices_temp)):
                                cross.append(oveDownLap(fiber_vertices_temp[j],temp1))
                            temp2=[i,x_UpL_temp,y_UpL_temp+L,x_DownL_temp,y_DownL_temp+L,x_DownR_temp,y_DownR_temp+L,x_UpR_temp,y_UpR_temp+L]
                            for j in range(len(fiber_vertices_temp)):
                                cross.append(oveDownLap(fiber_vertices_temp[j],temp2))                    
                            if max(cross)==1:
                                del cross
                                continue
                            else:
                                fiber_vertices.append([i,x_UpL,y_UpL,x_DownL,y_DownL,x_DownR,y_DownR,x_UpR,y_UpR])
                                fiber_vertices.append([i,x_UpL,y_UpL+L,x_DownL,y_DownL+L,x_DownR,y_DownR+L,x_UpR,y_UpR+L])
                                fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp,x_DownL_temp,y_DownL_temp,x_DownR_temp,y_DownR_temp,x_UpR_temp,y_UpR_temp])
                                fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp+L,x_DownL_temp,y_DownL_temp+L,x_DownR_temp,y_DownR_temp+L,x_UpR_temp,y_UpR_temp+L])                            
                                del cross
                                break
                    else:
                        cross=[]
                        if len(fiber_vertices)==0:
                            fiber_vertices.append([i,x_UpL,y_UpL,x_UpR,y_UpR,x_DownR,y_DownR,x_DownL,y_DownL])
                            fiber_vertices.append([i,x_UpL,y_UpL+L,x_UpR,y_UpR+L,x_DownR,y_DownR+L,x_DownL,y_DownL+L])
                            fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp,x_UpR_temp,y_UpR_temp,x_DownR_temp,y_DownR_temp,x_DownL_temp,y_DownL_temp])
                            fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp+L,x_UpR_temp,y_UpR_temp+L,x_DownR_temp,y_DownR_temp+L,x_DownL_temp,y_DownL_temp+L])                           
                            break
                        else:
                            temp1=[i,x_UpL_temp,y_UpL_temp,x_UpR_temp,y_UpR_temp,x_DownR_temp,y_DownR_temp,x_DownL_temp,y_DownL_temp]
                            for j in range(len(fiber_vertices_temp)):
                                cross.append(oveDownLap(fiber_vertices_temp[j],temp1))
                            temp2=[i,x_UpL_temp,y_UpL_temp+L,x_UpR_temp,y_UpR_temp+L,x_DownR_temp,y_DownR_temp+L,x_DownL_temp,y_DownL_temp+L]
                            for j in range(len(fiber_vertices_temp)):
                                cross.append(oveDownLap(fiber_vertices_temp[j],temp2))                    
                            if max(cross)==1:
                                del cross
                                continue
                            else:
                                fiber_vertices.append([i,x_UpL,y_UpL,x_UpR,y_UpR,x_DownR,y_DownR,x_DownL,y_DownL])
                                fiber_vertices.append([i,x_UpL,y_UpL+L,x_UpR,y_UpR+L,x_DownR,y_DownR+L,x_DownL,y_DownL+L])
                                fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp,x_UpR_temp,y_UpR_temp,x_DownR_temp,y_DownR_temp,x_DownL_temp,y_DownL_temp])
                                fiber_vertices_temp.append([i,x_UpL_temp,y_UpL_temp+L,x_UpR_temp,y_UpR_temp+L,x_DownR_temp,y_DownR_temp+L,x_DownL_temp,y_DownL_temp+L])                            
                                del cross
                                break                                         
                else:
                    continue
    ##############################开始建模
    
    
    #try:
    if TRUE:
        from part import * #第一步, 建立建模
        s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1000.0)   #定义模型的草图s
        s.rectangle(point1=(0.0, 0.0), point2=(bwidx, bwidy))               #指定两顶点画矩形
        p = mdb.models['Model-1'].Part(name='Part-1',dimensionality=TWO_D_PLANAR,type=DEFORMABLE_BODY)   #定义模型的部件part-1
        p.BaseShell(sketch=s)                                                #将s赋给p
        del mdb.models['Model-1'].sketches['__profile__']   #收回建模所占的环境内存
        
        s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1000.0)
        g = s1.geometry
        fr = open('D:\\PythonCode\\bishe\\result_bones.txt','w+')
        fr.write('CenterX\t\t\tCenterY\t\t\tAngle\n')
        for i in range(len(fiber_vertices)):
            if abs(disd([fiber_vertices[i][1],fiber_vertices[i][2]],[fiber_vertices[i][3],fiber_vertices[i][4]])-f_wid)<0.5*f_wid:
                x_LC=(fiber_vertices[i][1]+fiber_vertices[i][3])/2
                y_LC=(fiber_vertices[i][2]+fiber_vertices[i][4])/2
                x_DC=(fiber_vertices[i][3]+fiber_vertices[i][5])/2
                y_DC=(fiber_vertices[i][4]+fiber_vertices[i][6])/2
                x_RC=(fiber_vertices[i][5]+fiber_vertices[i][7])/2
                y_RC=(fiber_vertices[i][6]+fiber_vertices[i][8])/2
                x_UC=(fiber_vertices[i][7]+fiber_vertices[i][1])/2
                y_UC=(fiber_vertices[i][8]+fiber_vertices[i][2])/2
                s1.Line(point1=(fiber_vertices[i][3],fiber_vertices[i][4]),point2=(fiber_vertices[i][5],fiber_vertices[i][6]))
                s1.Line(point1=(fiber_vertices[i][7],fiber_vertices[i][8]),point2=(fiber_vertices[i][1],fiber_vertices[i][2]))
                flag=1
            else:
                x_LC=(fiber_vertices[i][1]+fiber_vertices[i][7])/2
                y_LC=(fiber_vertices[i][2]+fiber_vertices[i][8])/2
                x_DC=(fiber_vertices[i][7]+fiber_vertices[i][5])/2
                y_DC=(fiber_vertices[i][8]+fiber_vertices[i][6])/2
                x_RC=(fiber_vertices[i][5]+fiber_vertices[i][3])/2
                y_RC=(fiber_vertices[i][6]+fiber_vertices[i][4])/2
                x_UC=(fiber_vertices[i][3]+fiber_vertices[i][1])/2
                y_UC=(fiber_vertices[i][4]+fiber_vertices[i][2])/2
                s1.Line(point1=(fiber_vertices[i][1],fiber_vertices[i][2]),point2=(fiber_vertices[i][3],fiber_vertices[i][4]))
                s1.Line(point1=(fiber_vertices[i][5],fiber_vertices[i][6]),point2=(fiber_vertices[i][7],fiber_vertices[i][8]))
                flag=0
            k1=R/f_len
            rdef=pi/128
            x1t=x_LC+k1*(x_RC-x_LC)
            x2t=x_LC+(1-k1)*(x_RC-x_LC)
            y1t=y_LC+k1*(y_RC-y_LC)
            y2t=y_LC+(1-k1)*(y_RC-y_LC)
            ta=(y_RC-y_LC)/(x_RC-x_LC)
            b=y_RC-ta*x_RC
            a1=atan(ta)
            a0=asin(0.5*f_wid/R)
            angle=a1+a0
            xm=(fiber_vertices[i][1]+fiber_vertices[i][3]+fiber_vertices[i][5]+fiber_vertices[i][7])/4
            ym=(fiber_vertices[i][2]+fiber_vertices[i][4]+fiber_vertices[i][6]+fiber_vertices[i][8])/4
            
            s1.CircleByCenterPerimeter(center=(x_LC,y_LC), point1=(x_LC-c_rad,y_LC))
            s1.CircleByCenterPerimeter(center=(x_RC,y_RC), point1=(x_RC+c_rad,y_RC))
            
            s1.autoTrimCurve(curve1=g.findAt((fiber_vertices[i][1],fiber_vertices[i][2])), point1=(fiber_vertices[i][1],fiber_vertices[i][2]))
            s1.autoTrimCurve(curve1=g.findAt((fiber_vertices[i][3],fiber_vertices[i][4])), point1=(fiber_vertices[i][3],fiber_vertices[i][4]))
            s1.autoTrimCurve(curve1=g.findAt((fiber_vertices[i][5],fiber_vertices[i][6])), point1=(fiber_vertices[i][5],fiber_vertices[i][6]))
            s1.autoTrimCurve(curve1=g.findAt((fiber_vertices[i][7],fiber_vertices[i][8])), point1=(fiber_vertices[i][7],fiber_vertices[i][8]))
            
            s1.autoTrimCurve(curve1=g.findAt((x1t,y1t)), point1=(x1t,y1t))
            s1.autoTrimCurve(curve1=g.findAt((x2t,y2t)), point1=(x2t,y2t))
            if ta>=0:
                s1.FilletByRadius(radius=r_rad, curve1=g.findAt((x_DC,y_DC-0.0001)), nearPoint1=(x_DC,y_DC-0.0001), curve2=g.findAt((x_LC+R*cos(a1-a0-rdef),y_LC+R*sin(a1-a0-rdef))), nearPoint2=(x_LC+R*cos(a1-a0-rdef),y_LC+R*sin(a1-a0-rdef)))#左下
                s1.FilletByRadius(radius=r_rad, curve1=g.findAt((x_DC,y_DC-0.0001)), nearPoint1=(x_DC,y_DC-0.0001), curve2=g.findAt((x_RC-R*cos(a1+a0+rdef),y_RC-R*sin(a1+a0+rdef))), nearPoint2=(x_RC-R*cos(a1+a0+rdef),y_RC-R*sin(a1+a0+rdef)))#右下
                s1.FilletByRadius(radius=r_rad, curve1=g.findAt((x_UC,y_UC+0.0001)), nearPoint1=(x_UC,y_UC+0.0001), curve2=g.findAt((x_LC+R*cos(a1+a0+rdef),y_LC+R*sin(a1+a0+rdef))), nearPoint2=(x_LC+R*cos(a1+a0+rdef),y_LC+R*sin(a1+a0+rdef)))#左上
                s1.FilletByRadius(radius=r_rad, curve1=g.findAt((x_UC,y_UC+0.0001)), nearPoint1=(x_UC,y_UC+0.0001), curve2=g.findAt((x_RC-R*cos(a1-a0-rdef),y_RC-R*sin(a1-a0-rdef))), nearPoint2=(x_RC-R*cos(a1-a0-rdef),y_RC-R*sin(a1-a0-rdef)))#右上
            else:
                print 'miao'
            fr.write(str((fiber_vertices[i][1]+fiber_vertices[i][5])/2)+'\t'+str((fiber_vertices[i][2]+fiber_vertices[i][6])/2)+'\t')
            fr.write(str(180/pi*a1)+'\n')
        
        fr.close()
        p1 = mdb.models['Model-1'].parts['Part-1']
        pickedFaces = p1.faces[0:1]
        p1.PartitionFaceBySketch(faces=pickedFaces, sketch=s1)
        mdb.models['Model-1'].convertAllSketches()
        
        from material import *  #第二步, 材料定义
        from section import *
        mdb.models['Model-1'].Material(name='MATRIX')   #定义材料名称1
        mdb.models['Model-1'].materials['MATRIX'].Depvar(n=3)   #定义材料刚度
        mdb.models['Model-1'].materials['MATRIX'].UserDefinedField()
        mdb.models['Model-1'].materials['MATRIX'].Elastic(dependencies=2, table=((1100, 
            0.38, 0.0, 0.0), (110.0, 0.38, 1.0, 0.0), (110, 0.38, 0.0, 1.0, ),(110, 0.38, 1.0, 1.0)))
        mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1',material='MATRIX',thickness=1.0)  #定义截面1
        
        mdb.models['Model-1'].Material(name='FIBER')   #定义材料名称2
        mdb.models['Model-1'].materials['FIBER'].Depvar(n=3)   #定义材料刚度
        mdb.models['Model-1'].materials['FIBER'].UserDefinedField()
        mdb.models['Model-1'].materials['FIBER'].Elastic(dependencies=2, table=((220000, 
            0.25, 0.0, 0.0), (22000, 0.25, 1.0, 0.0), (22000, 0.25, 0.0, 1.0, ),(22000, 0.25, 1.0, 1.0)))
        mdb.models['Model-1'].HomogeneousSolidSection(name='Section-2',material='FIBER',thickness=1.0)  #定义截面2
        
        
        faces = mdb.models['Model-1'].parts['Part-1'].faces.findAt(((0.0, 0.0, 0.0), ))
        region =(faces, ) #以上两行找到包含点（0,0,0）的面，保存到region 
        mdb.models['Model-1'].parts['Part-1'].SectionAssignment(region=region, sectionName='Section-1') #截面属性附给选中的面region 
        
        f2=mdb.models['Model-1'].parts['Part-1'].faces
        miao=0
        flag=0
        for i in range(len(f2)):
            for j in range(len(faces)):
                if (f2[i]==faces[j]):
                    flag=1
            
            if flag==0:
                if miao:
                    faces4+=f2[i:i+1]
                else:
                    faces4=f2[i:i+1]
                    miao=1
            flag=0
        
        region2 =(faces4, )     #以上找到除faces以外的面，保存到region2 
        mdb.models['Model-1'].parts['Part-1'].SectionAssignment(region=region2, sectionName='Section-2') #截面属性2附给选中的面region2 
        
        from assembly import * #第三步，装配
        a1 = mdb.models['Model-1'].rootAssembly
        p = mdb.models['Model-1'].parts['Part-1']  #指定part-1
        a1.Instance(name='Part-1-1', part=p, dependent=OFF) #生成part-1对象的实体Part-1-1，independent网格在Instance上面
        
        
        from step import *  #第四步, 定义分析步
        mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial',
            timeIncrementationMethod=AUTOMATIC)  #定义一个固定增量的静态分析步
        mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValuesInStep(stepName='Step-1',
            variables=('S', 'U'))  #定义输出到ODB文件的数据(应力、位移)
        
        
        from mesh import *  #第五步, 网格划分控制
        
        #f1 = mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces
        #mdb.models['Model-1'].rootAssembly.setMeshControls(regions=f1, elemShape=TRI)
        
        elemType1 = mesh.ElemType(elemCode=CPE8, elemLibrary=STANDARD)
        elemType2 = mesh.ElemType(elemCode=CPE6, elemLibrary=STANDARD)
        faces = mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces
        pickedRegions =(faces, )
        mdb.models['Model-1'].rootAssembly.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))   #定义两种网格类型
        
        #size0=float(getInput("Input the mesh size:","0.1"))
        #size0=0.2
        m=mdb.models['Model-1']
        r=m.rootAssembly
        pickedEdges=a1.instances['Part-1-1'].edges
        a1.seedEdgeBySize(edges=pickedEdges, size=size0,constraint=FIXED) #撒网格种子
        partInstances =(a1.instances['Part-1-1'], )
        a1.generateMesh(regions=partInstances) #给partInstances划分网格
        
        
        
        from interaction import *   #第六步, 定义多点约束条件-----MPC
        m=mdb.models['Model-1']
        r=m.rootAssembly
        node=r.instances['Part-1-1'].nodes
        nel=[]
        ner=[]
        neu=[]
        ned=[]
        for i in range(len(node)):
            x=node[i].coordinates[0]
            y=node[i].coordinates[1]
            flag=(x-bwidx)*(x-0)*(y-bwidy)*(y-0)
            if abs(flag)<0.0001:
                if (abs(y-bwidy)>0.01)and(abs(y-0)>0.01):
                    if (abs(x-0)<0.0001):
                        nel.append(i)
                    if (abs(x-bwidx)<0.0001):
                        ner.append(i)
                if (abs(x-bwidx)>0.01)and(abs(x-0)>0.01):
                    if (abs(y-0)<0.0001):
                        ned.append(i)
                    if (abs(y-bwidy)<0.0001):
                        neu.append(i)
                
                if (abs(x-0)<0.01)and(abs(y-0)<0.01):
                    r.Set(nodes=node[i:i+1],name='set-01')
                elif(abs(x-bwidx)<0.01)and(abs(y-0)<0.01):
                    r.Set(nodes=node[i:i+1],name='set-02')
                elif(abs(x-0)<0.01)and(abs(y-bwidy)<0.01):
                    r.Set(nodes=node[i:i+1],name='set-03')
                elif(abs(x-bwidx)<0.01)and(abs(y-bwidy)<0.01):
                    r.Set(nodes=node[i:i+1],name='set-04')
        
        
        m.Equation(name='eq-00',terms=((1,'set-04',1),(-1,'set-02',1),(-1,'set-03',1))) #定义角点的MPC
        m.Equation(name='eq-01',terms=((1,'set-04',2),(-1,'set-02',2),(-1,'set-03',2)))
        
        #-----------------------------定义其他边界点的MPC----------------
        
        i=0
        
        for n in range(len(nel)):
            x0=node[nel[n]].coordinates[0]
            y0=node[nel[n]].coordinates[1]
            for j in range(len(ner)):
                x1=node[ner[j]].coordinates[0]
                y1=node[ner[j]].coordinates[1]
                if (abs(y0-y1)<0.3*size0):
                    r.Set(nodes=node[nel[n]:nel[n]+1],name='set-l-'+str(i))
                    r.Set(nodes=node[ner[j]:ner[j]+1],name='set-r-'+str(i))
                    m.Equation(name='eq-lr-x-'+str(i),terms=((1,'set-r-'+str(i),1),(-1,'set-02',1),(-1,'set-l-'+str(i),1)))
                    m.Equation(name='eq-lr-y-'+str(i),terms=((1,'set-r-'+str(i),2),(-1,'set-02',2),(-1,'set-l-'+str(i),2)))
                    i=i+1
                    break
        
        i=0
        for n in range(len(ned)):
            x0=node[ned[n]].coordinates[0]
            y0=node[ned[n]].coordinates[1]
            for j in range(len(neu)):
                x1=node[neu[j]].coordinates[0]
                y1=node[neu[j]].coordinates[1]
                if (abs(x0-x1)<0.3*size0):
                    r.Set(nodes=node[ned[n]:ned[n]+1],name='set-d-'+str(i))
                    r.Set(nodes=node[neu[j]:neu[j]+1],name='set-u-'+str(i))
                    m.Equation(name='eq-ud-x-'+str(i),terms=((1,'set-u-'+str(i),1),(-1,'set-03',1),(-1,'set-d-'+str(i),1)))
                    m.Equation(name='eq-ud-y-'+str(i),terms=((1,'set-u-'+str(i),2),(-1,'set-03',2),(-1,'set-d-'+str(i),2)))
                    i=i+1
                    break
        
        print "i=",i    
        #--------------------------------------------------------------    
        from load import *   #第七步, 荷载边界定义
        m=mdb.models['Model-1']                  
        region = m.rootAssembly.sets['set-01']    #选中固支节点，保存到region
        m.DisplacementBC(name='BC-1', createStepName='Initial',region=region,
            u1=SET, u2=SET, ur3=SET, amplitude=UNSET,distributionType=UNIFORM, localCsys=None) #定义固支边界
        
        region = m.rootAssembly.sets['set-02']    #选中简支节点，保存到region
        m.DisplacementBC(name='BC-2', createStepName='Step-1',region=region,
            u1=(bwidx/100), u2=SET, ur3=SET, amplitude=UNSET,distributionType=UNIFORM, localCsys=None) #定义简支边界
        
        region = m.rootAssembly.sets['set-03']    #选中加载节点，保存到region
        m.DisplacementBC(name='BC-3', createStepName='Step-1',region=region,
            u1=SET, u2=UNSET, ur3=SET, amplitude=UNSET, fixed=OFF,distributionType=UNIFORM, localCsys=None) #定义位移载荷
        
        
        
        #-----------------------------------------第八步，生成任务以及其他杂项功能
        regionDef=mdb.models['Model-1'].rootAssembly.sets['set-02']
        mdb.models['Model-1'].historyOutputRequests['H-Output-1'].setValues(variables=(
            'U1', 'RF1'), region=regionDef, 
            sectionPoints=DEFAULT, rebar=EXCLUDE)
        regionDef=mdb.models['Model-1'].rootAssembly.sets['set-03']
        mdb.models['Model-1'].HistoryOutputRequest(name='H-Output-2', 
            createStepName='Step-1', variables=('U2', 'RF2'), region=regionDef, 
            sectionPoints=DEFAULT, rebar=EXCLUDE)
        #-----------------------------------------第九步，提交作业
        mdb.Job(name=job_name, model='Model-1', description='', type=ANALYSIS, 
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, 
            scratch='', multiprocessingMode=DEFAULT, numCpus=1)
        #mdb.jobs[job_name].submit(consistencyChecking=OFF)
        mdb.saveAs(Pathname+'\\'+job_name)
    #except:
    #    print('ERROR')

