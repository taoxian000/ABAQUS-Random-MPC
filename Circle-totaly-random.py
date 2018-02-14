# -*- coding: utf-8 -*-
#filename:abaqus_1.py
####################################调用模块
from random import*   
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
from abaqus import backwardCompatibility
backwardCompatibility.setValues(reportDeprecated=False)
import os
executeOnCaeStartup()
###################################设定参数
if os.path.exists('D:\\PythonCode\\bishe\\circle_force.txt'):
    os.remove('D:\\PythonCode\\bishe\\circle_force.txt')

f = open('D:\\PythonCode\\bishe\\circle.txt','r')
ffo = open('D:\\PythonCode\\bishe\\circle_force.txt','a+')
ffo.write('name\t\tRF1\t\tU1\t\tRF2\t\tU2\n')
#i=0
for line in f:
    #i=i+1
    #print (i)
    data=line.split()
    bwidx=float(data[0])    #基体宽度
    bwidy=float(data[1])    #基体长度
    f_r=float(data[2])      #纤维半径
    f_dis=float(data[3])    #纤维最小间距一半
    f_num=int(data[4])      #纤维数目
    size0=float(data[5])    #网格尺寸
    job_name=data[6]        #工作名称
    Pathname=data[7]        #存储路径
    os.chdir(Pathname)
    
    ################################随机生成纤维束的圆心坐标xy
    r0 = f_r
    r = f_r+f_dis
    x = bwidx*random()
    y = bwidy*random()
    xy = [(x,y)]
    del xy[0]
    for i in range(f_num):
        flag=1  #数值为1的时候是重叠的
        while flag==1:
            x = bwidx*random()
            y = bwidy*random()
            flag = 0
            #######################注意修改这一行
            if (1.2<x<2.4)or(1.2<y<2.4)or(bwidx-2.4<x<bwidx-1.2)or(bwidy-2.4<y<bwidy-1.2):
                flag=1 
            for j in range(len(xy)):#数列XY的长度
                dis=(x-xy[j][0])**2+(y-xy[j][1])**2                 #中间部分的纤维
                if dis < ((r+r0)**2):
                    flag=1
                if (x+r0 > bwidx):   
                    dis=(x-bwidx-xy[j][0])**2+(y-xy[j][1])**2       #右边界的纤维
                    if dis < ((r0+r)**2):
                        flag=1
                    dis=(x-bwidx-xy[j][0])**2+(y-bwidy-xy[j][1])**2 #右上角的纤维
                    if dis < ((r0+r)**2):
                        flag=1
                    dis=(x-bwidx-xy[j][0])**2+(y+bwidy-xy[j][1])**2 #右下角的纤维
                    if dis < ((r0+r)**2):
                        flag=1
                if (x-r0 < 0):
                    dis=(x+bwidx-xy[j][0])**2+(y-xy[j][1])**2       #左边界的纤维
                    if dis < ((r0+r)**2):
                        flag=1
                    dis=(x+bwidx-xy[j][0])**2+(y+bwidy-xy[j][1])**2 #左下角的纤维
                    if dis < ((r0+r)**2):
                        flag=1
                    dis=(x+bwidx-xy[j][0])**2+(y-bwidy-xy[j][1])**2 #左上角的纤维
                    if dis < ((r0+r)**2):
                        flag=1
                if (y+r0 > bwidy):
                    dis=(x-xy[j][0])**2+(y-bwidy-xy[j][1])**2       #上边界的纤维
                    if dis < ((r0+r)**2):
                        flag=1
                if (y-r0 < 0):
                    dis=(x-xy[j][0])**2+(y+bwidy-xy[j][1])**2       #下边界的纤维
                    if dis < ((r0+r)**2):
                        flag=1
                    
        xy.append((x,y))
        if (x+r0 > bwidx):##############补充超出边界图形 
            xy.append((x-bwidx,y))
            if (y+r0 > bwidy):
                xy.append((x-bwidx,y-bwidy))
            if (y-r0 < 0):
                xy.append((x-bwidx,y+bwidy))
        if (y+r0 > bwidy):
            xy.append((x,y-bwidy))
        if (x-r0 < 0):
            xy.append((x+bwidx,y))
            if (y-r0 < 0):
                xy.append((x+bwidx,y+bwidy))
            if (y+r0 > bwidy):
                xy.append((x+bwidx,y-bwidy))
        if (y-r0 < 0):
            xy.append((x,y+bwidy))
    
    
####################################开始建模
    
    try:
        Mdb()
        from part import *     #第一步, 建立建模 
        s = mdb.models['Model-1'].Sketch(name='__profile__', sheetSize=1000.0)  #定义模型的草图s
        s.rectangle(point1=(0.0, 0.0), point2=(bwidx, bwidy))                   #指定两顶点画矩形
        p = mdb.models['Model-1'].Part(name='Part-1',dimensionality=TWO_D_PLANAR,type=DEFORMABLE_BODY)  #定义模型的部件part-1
        p.BaseShell(sketch=s)                                                        #将s赋给p
        del mdb.models['Model-1'].sketches['__profile__']   #收回建模所占的环境内存
        
        s1 = mdb.models['Model-1'].Sketch(name='__profile__', sheetSize=1000.0)
        fr = open('D:\\PythonCode\\bishe\\result_circle_'+job_name+'.txt','w+')
        fr.write('CenterX\t\t\tCenterY\n')
        for i in range(len(xy)):
            s1.CircleByCenterPerimeter(center=xy[i], point1=(xy[i][0]+r0,xy[i][1]))      #指定圆心和圆上一点画圆n个
            fr.write(str(xy[i][0])+'\t'+str(xy[i][1])+'\n')
        
        fr.close()
        p1 = mdb.models['Model-1'].parts['Part-1']
        pickedFaces = p1.faces[0:1]
        p1.PartitionFaceBySketch(faces=pickedFaces, sketch=s1)
        mdb.models['Model-1'].convertAllSketches()
        
        
        from material import *       #第二步, 材料定义
        from section import *
        mdb.models['Model-1'].Material(name='Material-1')   #基体材料1
        mdb.models['Model-1'].materials['Material-1'].Elastic(table=((1000.0, 0.38), ))  #基体刚度
        mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1',material='Material-1',thickness=1.0)  #基体截面
        
        mdb.models['Model-1'].Material(name='Material-2')   #纤维材料1
        mdb.models['Model-1'].materials['Material-2'].Elastic(table=((194000.0, 0.285), ))  #纤维刚度
        mdb.models['Model-1'].HomogeneousSolidSection(name='Section-2',material='Material-2',thickness=1.0)  #纤维截面
        
        for i in range(len(xy)):
            if ((xy[i][0]>r0+0.01*r0) and (xy[i][1]>r0+0.01*r0) and (xy[i][0]<bwidx-r0-0.01*r0) and (xy[i][1]<bwidy-r0-0.01*r0)):
                j=i
        
        faces = mdb.models['Model-1'].parts['Part-1'].faces.findAt(((xy[j][0]-r0-0.005*r0, xy[j][1], 0.0), ))#找到基体
        
        for i in range(len(xy)):#避免边角位置不能定义
            if (((xy[i][0])**2+(xy[i][1])**2 >= r0**2) and ((xy[i][0]-0) <= r0) and (xy[i][0] > 0) and ((xy[i][1]-0) <= r0) and (xy[i][1] > 0)):
                faces2=mdb.models['Model-1'].parts['Part-1'].faces.findAt(((0.0, 0.0, 0.0), ))
                faces=faces+faces2
            if (((xy[i][0]-bwidx)**2+(xy[i][1])**2 >= r0**2) and (-(xy[i][0]-bwidx) <= r0) and ((xy[i][1]-0) <= r0) and (xy[i][1] > 0) and (xy[i][0] < bwidx)):
                faces2=mdb.models['Model-1'].parts['Part-1'].faces.findAt(((bwidx, 0.0, 0.0), ))
                faces=faces+faces2
            if (((xy[i][0]-bwidx)**2+(xy[i][1]-bwidy)**2 >= r0**2) and (-(xy[i][0]-bwidx) <= r0) and (-(xy[i][1]-bwidy) <= r0) and (xy[i][0] < bwidx) and (xy[i][1] < bwidy)):
                faces2=mdb.models['Model-1'].parts['Part-1'].faces.findAt(((bwidx, bwidy, 0.0), ))
                faces=faces+faces2
            if (((xy[i][0])**2+(xy[i][1]-bwidy)**2 >= r0**2) and ((xy[i][0]-0) <= r0) and (-(xy[i][1]-bwidy) <= r0) and (xy[i][1] < bwidy) and (xy[i][0] > 0)):
                faces2=mdb.models['Model-1'].parts['Part-1'].faces.findAt(((0.0, bwidy, 0.0), ))
                faces=faces+faces2
        
        region = (faces, )#以上两行找基体的面，保存到region
        mdb.models['Model-1'].parts['Part-1'].SectionAssignment(region=region, sectionName='Section-1') ##截面属性附给选中的面region
        
        f2=mdb.models['Model-1'].parts['Part-1'].faces
        miao=0
        flag=0
        for i in range(len(f2)):
            for j in range(len(faces)):
                if (f2[i]==faces[j]):
                    flag=1
            
            if flag==0:
                if miao:
                    faces3+=f2[i:i+1]
                else:
                    faces3=f2[i:i+1]
                    miao=1
            flag=0
        
        region2 =(faces3, )     #以上找到除faces以外的面，保存到region2 
        mdb.models['Model-1'].parts['Part-1'].SectionAssignment(region=region2, sectionName='Section-2') #截面属性2附给选中的面region2 
        
        from assembly import *     #第三步，装配
        a1 = mdb.models['Model-1'].rootAssembly
        p = mdb.models['Model-1'].parts['Part-1']  ##指定part-1
        a1.Instance(name='Part-1-1', part=p, dependent=OFF) #生成part-1对象的实体Part-1-1，independent网格在Instance上面
        
        
        from step import *  #第四步, 定义分析步
        mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial',
            timeIncrementationMethod=AUTOMATIC)  #定义一个固定增量的静态分析步
        mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValuesInStep(stepName='Step-1',
            variables=('S', 'U', 'COORD'))   #定义输出到ODB文件的数据(应力、位移)
        
        
        from mesh import *  #第五步, 网格划分控制
        
        #f1 = mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces
        #mdb.models['Model-1'].rootAssembly.setMeshControls(regions=f1, elemShape=TRI)
        
        elemType1 = mesh.ElemType(elemCode=CPE8, elemLibrary=STANDARD)
        elemType2 = mesh.ElemType(elemCode=CPE6, elemLibrary=STANDARD)
        faces = mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces
        pickedRegions =(faces, )  #定义两种网格类型
        mdb.models['Model-1'].rootAssembly.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))  
        
        #size0=float(getInput("Input the mesh size:","0.1"))
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
        
        #定义角点的MPC
        m.Equation(name='eq-00',terms=((1,'set-04',1),(-1,'set-02',1),(-1,'set-03',1))) 
        m.Equation(name='eq-01',terms=((1,'set-04',2),(-1,'set-02',2),(-1,'set-03',2)))
        
#-----------------------------定义其他边界点的MPC----------------
        i=0
        
        for n in range(len(nel)):
            x0=node[nel[n]].coordinates[0]
            y0=node[nel[n]].coordinates[1]
            for j in range(len(ner)):
                x1=node[ner[j]].coordinates[0]
                y1=node[ner[j]].coordinates[1]
                if (abs(y0-y1)<0.1*size0):
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
                if (abs(x0-x1)<0.1*size0):
                    r.Set(nodes=node[ned[n]:ned[n]+1],name='set-d-'+str(i))
                    r.Set(nodes=node[neu[j]:neu[j]+1],name='set-u-'+str(i))
                    m.Equation(name='eq-ud-x-'+str(i),terms=((1,'set-u-'+str(i),1),(-1,'set-03',1),(-1,'set-d-'+str(i),1)))
                    m.Equation(name='eq-ud-y-'+str(i),terms=((1,'set-u-'+str(i),2),(-1,'set-03',2),(-1,'set-d-'+str(i),2)))
                    i=i+1
                    break
        
        print ("i=",i)    
        #--------------------------------------------------------------    
        from load import *   #第七步, 荷载边界定义
        m=mdb.models['Model-1']                  
        region = m.rootAssembly.sets['set-01']    #选中固支节点，保存到region
        m.DisplacementBC(name='BC-1', createStepName='Initial',region=region,
            u1=SET, u2=SET, ur3=SET, amplitude=UNSET,distributionType=UNIFORM, localCsys=None) #定义固支边界
        
        region = m.rootAssembly.sets['set-02']   #选中简支节点，保存到region
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

