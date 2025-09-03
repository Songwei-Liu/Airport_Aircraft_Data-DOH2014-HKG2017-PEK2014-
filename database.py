#9.8.2017
#for piec-wise linear speed profile stored in database
import math

def readDbase(filename):
    file=open(filename, "r")
    dbase={}
    
    for line in file:
        buf=line.split('\t')
        dbase[float(buf[0])]=[float(b) for b in buf[1:-1]]
        
    return dbase
#@profile


def calculateEdgeTimes(startTime,segment,dbEntry,weightClass,segmentEdges,G,multiCosts):
    #segment=[id_seg in_sp en_sp length type holding_time]
    verbose=False
    objectives = [0,0,0]
    objSeg = []
    edgeTimes = {e[0]:[] for e in segmentEdges}
    pop = []
    extrapop = []
    length=segment[3]
    solCount=int(len(dbEntry)/10)
    validSols=[True]*solCount
    
    #for n number of paralel edges with diff costs change here: solCount,n
    if multiCosts==-1:
        solRange=range(solCount-1,solCount)
    elif isinstance(multiCosts,list):
        
        if segment[4]!=2: #turn
            calculatedCosts=[dbEntry[solCounter]*multiCosts[0]+dbEntry[solCount+solCounter]*multiCosts[1] for solCounter in range(solCount)] 
            minSolIndex=calculatedCosts.index(min(calculatedCosts))
            solRange=range(minSolIndex,minSolIndex+1)
        else:
            solRange=range(1)
                   
    else:
        solRange=range(min([solCount,multiCosts]))
    for solCounter in solRange:
        tempObjSeg = []
        tempPop =[]
        tempExtraPop =[]
        if segment[4]==1 and segment[1]>0:
            #straigth segment and in database and initial speed > 0 (=5.14)
            tempObjSeg.append(dbEntry[solCounter]) #obj1  # Songwei - here, solCount is constant, solCounter increases
            tempObjSeg.append(dbEntry[solCount+solCounter]) #obj2
            tempObjSeg.append(dbEntry[2*solCount+solCounter]) #obj3
            tempPop.append(dbEntry[3*solCount+solCounter]) 
            tempPop.append(dbEntry[4*solCount+solCounter]) 
            tempPop.append(dbEntry[5*solCount+solCounter]) 
            tempPop.append(dbEntry[6*solCount+solCounter]) 
            
            tempExtraPop.append(dbEntry[7*solCount+solCounter]) 
            tempExtraPop.append(dbEntry[8*solCount+solCounter]) 
            tempExtraPop.append(dbEntry[9*solCount+solCounter]) 
            #tempExtraPop.append(dbEntry[10*solCount+solCounter])
        elif segment[4]==2:
            #turning segment has all pop, extrapop = 0
            turnFuel=0.0
            hc=0.0
            if weightClass=='light':
                turnFuel = 0.0240
                hc = 20.040162574676550
            elif weightClass=='medium':
                turnFuel = 0.1010
                hc = 9.36999999988024
            elif weightClass=='heavy':
                turnFuel = 0.2280
                hc = 1.400000147234979
            tempObjSeg.append(length/5.14); #obj1
            tempObjSeg.append((length/5.14)*2*turnFuel); #obj2
            tempObjSeg.append((length/5.14)*2*turnFuel*hc); #obj3
            tempPop.append(0.0); 
            tempPop.append(0.0); 
            tempPop.append(segment[3]); 
            tempPop.append(0.0); 
            
            tempExtraPop.append(0.0); 
            tempExtraPop.append(0.0); 
            tempExtraPop.append(0.0); 
            #tempExtraPop.append(0.0);         
        elif segment[4]==1 and segment[1]==0:
            #straigth segment with initial speed = 0, breakaway
            tempObjSeg.append(dbEntry[solCounter]) #obj1
            tempObjSeg.append(dbEntry[solCount+solCounter]) #obj2
            tempObjSeg.append(dbEntry[2*solCount+solCounter]) #obj3
            tempPop.append(dbEntry[3*solCount+solCounter]) 
            tempPop.append(dbEntry[4*solCount+solCounter]) 
            tempPop.append(dbEntry[5*solCount+solCounter]) 
            tempPop.append(dbEntry[6*solCount+solCounter]) 

            tempExtraPop.append(dbEntry[7*solCount+solCounter]) 
            tempExtraPop.append(dbEntry[8*solCount+solCounter]) 
            tempExtraPop.append(dbEntry[9*solCount+solCounter]) 
            #tempExtraPop.append(dbEntry[10*solCount+solCounter]) 
        elif segment[4]==3:
            tempObjSeg.append(dbEntry[solCounter]) #obj1
            tempObjSeg.append(dbEntry[solCount+solCounter]) #obj2
            tempObjSeg.append(dbEntry[2*solCount+solCounter]) #obj3
            tempPop.append(dbEntry[3*solCount+solCounter]) 
            tempPop.append(dbEntry[4*solCount+solCounter]) 
            tempPop.append(dbEntry[5*solCount+solCounter]) 
            tempPop.append(dbEntry[6*solCount+solCounter]) 

            tempExtraPop.append(dbEntry[7*solCount+solCounter]) 
            tempExtraPop.append(dbEntry[8*solCount+solCounter]) 
            tempExtraPop.append(dbEntry[9*solCount+solCounter]) 
            #tempExtraPop.append(dbEntry[10*solCount+solCounter]) 
        else:
            tempObjSeg.append(length/5.14); #obj1
            tempObjSeg.append(0.0) #obj2
            tempObjSeg.append(0.0) #obj3
            tempPop.append(0.0) 
            tempPop.append(0.0) 
            tempPop.append(0.0) 
            tempPop.append(0.0) 

            tempExtraPop.append(0.0) 
            tempExtraPop.append(0.0) 
            tempExtraPop.append(0.0) 
            #tempExtraPop.append(0.0) 

        #tempObjSeg[:]=[round(o,1) for o in tempObjSeg]
        objSeg.append(tempObjSeg)
        pop.append(tempPop)
        extrapop.append(tempExtraPop)
        #reconstruct speed profile
        d4 = length - (tempPop[1] + tempPop[2] + tempExtraPop[0])
        d3 = tempExtraPop[0]
        d2 = tempPop[2]
        d1 = tempPop[1]
        initial_speed = segment[1]
        a1 = tempPop[0]
        a2 = tempExtraPop[1]
        if a2<= 10*5**(-4):
            a2=0.0
        a3 = 0.98
        if a1<= 10*5**(-4):
            t1=0.0
            a1=0.0
        else:
            t1 = (-2*initial_speed+math.sqrt(4*(initial_speed**2)+8*a1*d1))/(2*a1)
        #find out the highest speed when reaching the end of the first phase
        sp_f = initial_speed + a1*t1
        #t2
        t2 = d2 / sp_f
        #t3
        if a2==0.0 and d3 == 0.0:
            t3=0

        elif a2==0.0 and d3 != 0.0:
            cs = initial_speed + a1 * t1 + a2 * t2
            t3 = d3/cs

        else:
            # for calculate purpose
            abs1 = 4*(sp_f**2)-8*a2*d3
            if (abs(abs1) < 0.01):
                abs1 = 0.0
            t3 = (2*sp_f-math.sqrt(abs1))/(2*a2)
        # t4
        sp_f4 = sp_f - a2 * t3
        
        if segment[4]==2:
            t4 = 0
        elif (a3 == 0.0 and d4 == 0.0):
            t4 = 0.0

        elif (a3 == 0.0 and d4 !=0.0):
            #//% speed from last phase
            ls = initial_speed + a1*t1 - a2*t3
            t4 = d4/ls

        elif segment[2]==0.0:
            #last segment, a/c will stop
            t4 = sp_f4/a3

        else:
            abs1 = 4*((sp_f4**2))-8*a3*d4
            if (abs(abs1) < 0.01):
    
                abs1 = 0.0
    
            #print(a3,abs1)
            t4 = (2*sp_f4-math.sqrt(abs1))/(2*a3)

        #//% time
        t = t1 + t2 + t3 + t4
        if verbose==True:
            print('t',t1,t2,t3,t4, t)
            print('dist', d1+d2+d3+d4)
        #
        
        #
        distance=[]
        #for t in range(int(t1*100)):
            #t=t/100.0
            #v=initial_speed+a1*t
            #s = initial_speed*t+0.5*a1*(t**2)
            #distance.append([s,t])
            ##print s, t, a1,v
        #if verbose==True:    
            #print 'sd1',s,d1
        #v=initial_speed+a1*t1
        #s = initial_speed*t1+0.5*a1*(t1**2)
        #distance.append([s,t1]) 
        ##print 'd1', distance
        ##print t2
        #for t in range(int(t2*100)):
            #t=t/100.0
            #v=initial_speed+a1*t1
            #s=v*t
            #distance.append([d1+s,t+t1])
            ##print s,t
        #if verbose==True:
            #print 'sd2',s,d2    
        #s = v*t2
        #distance.append([d1+s,t2+t1])
        ##print 'd2', distance    
        ##print len(distance)

        #for t in range(int(t3*100)):
            #t=t/100.0
            #v=initial_speed+a1*t1
            #s = (initial_speed+ a1*t1)*t-0.5*a2*(t**2)
            #distance.append([d1+d2+s,t+t1+t2])
        
        #if verbose==True:
            #print 'sd3',s,d3
        
        #s = (initial_speed+ a1*t1)*t3-0.5*a2*(t3**2)
        #distance.append([d1+d2+s,t1+t2+t3]) 
        ##print 'd3', distance
        #for t in range(int(t4*100)):
            #t=t/100.0
            #v3=initial_speed+a1*t1-a2*t3
            #s=v3*t-0.5*a3*(t**2)
            #distance.append([d1+d2+d3+s,t+t1+t2+t3])
        
        #if verbose==True:
            #print 'sd4',s,d4, v3
        #v3=initial_speed+a1*t1-a2*t3    
        #s=v3*t4-0.5*a3*(t4**2)
        #distance.append([d1+d2+d3+s,t2+t1+t3+t4])
        #for dd in distance:
            #print dd
        t_start=startTime
        #print 't_start', t_start
        t_end=startTime
        
        for edge_index,edge in enumerate(segmentEdges):
            d_start = sum([float(e[4]) for e in segmentEdges[0:edge_index]])
            d_end = sum([float(e[4]) for e in segmentEdges[0:edge_index+1]])
            #print 'distance', distance,d_end
            #
            #% check if the current edge is within the first phase (acceleration phase) of the segment
            if d_end<=d1:
 
                #//% calculate the time needed for the current edges
                if (a1==0):
                    t = 0.0
                else:

                    t = (-2*initial_speed+math.sqrt(4*((initial_speed**2))+8*a1*d_end))/(2*a1)

                t_end = startTime+t
            
            #//% check if the current edge is within the second phase (constant speed)
            elif d_end>d1 and d_end<=(d1+d2):
                #print 'constant'
                t = ((d_end-d1)/sp_f)
                t_end = startTime+t1+t
                #print t1,t
            #//% check if the current edge is within the third phase (slow deceleration phase)
            elif d_end>(d1+d2) and d_end<=(d1+d2+d3):
                #print 'brake',d_end-(d1+d2),a2
                d_remain=d_end-(d1+d2)
                if a2==0.0 and d_remain == 0.0:
                    t=0

                elif a2==0.0 and d_remain != 0.0:

                    cs = initial_speed + a1 * t1 + a2 * t2
                    t = d_remain/cs

                else:

                    # for calculate purpose
                    abs1 = 4*(sp_f**2)-8*a2*d_remain
                    if (abs(abs1) < 0.01):
    
                        abs1 = 0.0
    
        
    
                    t = (2*sp_f-math.sqrt(abs1))/(2*a2)
                t_end = startTime+t1+t2+t
            #//% check if the current edge is within the fourth phase (fast deceleration phase)
            elif d_end>(d1+d2+d3):
                d_remain=d_end-(d1+d2+d3)
                if segment[4]==2:
                    t = 0
                elif (a3 == 0.0 and d_remain == 0.0):

                    t = 0.0

                elif (a3 == 0.0 and d_remain !=0.0):

                    #//% speed from last phase
                    ls = initial_speed + a1*t1 - a2*t3
                    t = d_remain/ls

                elif segment[2]==0.0:
                    #last segment, a/c will stop

                    t = sp_f4/a3

                else:

                    #//% for calculate purpose
                
                    abs1 = 4*((sp_f4**2))-8*a3*d_remain
                    if (abs(abs1) < 0.01):
            
                        abs1 = 0.0
            
            
                    t = (2*sp_f4-math.sqrt(abs1))/(2*a3)  
                t_end=startTime+t1+t2+t3+t
                #
            #for d in distance:
                #if d[0]>=d_start:
                    #t_start=d[1]+startTime
                    #break
            #for d in distance:
                #if d[0]>=d_end or (d[0]-d_end)<0.01:
                    #t_end=d[1]+startTime
                    #break

            if verbose==True:
                print('d', d_start, d_end, t_start, t_end)
            if t_start>t_end:
                print(t_start, t_end, startTime,t1,t2,t3,t)
                raise ValueError('t_start>t_end')                
            edgeTimes[edge[0]].append([t_start,t_end])
            timeWindow = G[edge[1]][edge[2]]['tw']
            valid=False
            for tw in timeWindow:
                if t_start>=tw[0] and t_end<=tw[1]:
                    valid=True
                    break
                    
            if valid==False:
                validSols[solCounter]=False
            
            t_start=t_end
    
    return objSeg,pop,extrapop, validSols, edgeTimes


def calculateTurnFuel(length,weightClass):
    turnFuel=0.0
    hc=0.0
    if weightClass=='light':
        turnFuel = 0.0240
        hc = 20.040162574676550
    elif weightClass=='medium':
        turnFuel = 0.1010
        hc = 9.36999999988024
    elif weightClass=='heavy':
        turnFuel = 0.2280
        hc = 1.400000147234979
    return (length/15.43,(length/15.43)*2*turnFuel,(length/15.43)*2*turnFuel*hc)

#import networkx as nx
#from gm_parse import gm_parser
#angles, nodes, edges = gm_parser('./results/data/pek5.txt','./results/data/PEK5_angles.txt')
#G=nx.DiGraph()
#for edge in edges:
    #if edge[5] <> 'runway':
        ##for testing
        #if edge[0]=='2058':
            
            #G.add_edge(edge[1],edge[2],edge_id=edge[0],c=(float(edge[4]),0),tw=[[0.0,float('inf')]],length=float(edge[4]))
            #G.add_edge(edge[2],edge[1],edge_id=edge[0],c=(float(edge[4]),0),tw=[[0.0,float('inf')]],length=float(edge[4]))
        #else:
            #G.add_edge(edge[1],edge[2],edge_id=edge[0],c=(float(edge[4]),0),tw=[[0.0,float('inf')]],length=float(edge[4]))
            #G.add_edge(edge[2],edge[1],edge_id=edge[0],c=(float(edge[4]),0),tw=[[0.0,float('inf')]],length=float(edge[4]))  
##dbase= readDbase('/home/michal/Documents/lincoln/temp/HKG/dbase_hkg_medium.txt')
#dbases={'medium':{'straight':readDbase('/home/michal/Documents/lincoln/temp/HKG/dbase_pek_medium.txt'),'breakaway':readDbase('/home/michal/Documents/lincoln/temp/HKG/dbase_hkg_breakaway_medium.txt'),'hold':readDbase('/home/michal/Documents/lincoln/temp/HKG/dbase_hkg_hold_medium.txt')}}
#dbases['heavy']={'straight':readDbase('/home/michal/Documents/lincoln/temp/HKG/dbase_pek_heavy.txt'),'breakaway':readDbase('/home/michal/Documents/lincoln/temp/HKG/dbase_hkg_breakaway_heavy.txt'),'hold':readDbase('/home/michal/Documents/lincoln/temp/HKG/dbase_hkg_hold_heavy.txt')}
#cProfile.run('calculateEdgeTimes(0,[0,5.14,5.14,129.0,1,0],dbases["medium"]["straight"][129.0],"medium",[["900", "2063", "5024", "0", "128.92399038067853", "", "128.92399038067853", "C25"]],G,1)')
#cProfile.run('calculateEdgeTimes(0,[0,5.14,5.14,500.0,1,0],dbase["medium"][500.0],"medium",[[0,0,0,0,50] for i in range(10)],[[[0.0,float("inf")]]]*10)')
#objSeg,pop,extrapop,validSols= calculateEdgeTimes(0,[0,5.14,5.14,500.0,1,0],dbase[500.0],'medium',[[0,0,0,0,50] for i in range(10)],[[[0.0,float('inf')]]]*10)
#print len(objSeg), objSeg
#print extrapop
#print validSols