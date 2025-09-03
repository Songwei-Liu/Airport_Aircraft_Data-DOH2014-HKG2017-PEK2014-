import math

def expandSegments_kqpptw(startingEdge,nodes,edges,predecessorNode,edgeSuccessors):

    def get_successor(edge,edges):
        return [e for e in edges if (edge[1] in e[1:3] or edge[2] in e[1:3]) and e[0]!=edge[0]]


    def angle(x1,y1,x2,y2,x3,y3):
        #print x1,y1,x2,y2,x3,y3
        angle = 0.0
        x1 = float(x1)
        x2 = float(x2)
        y1 = float(y1)
        y2 = float(y2)
        x3 = float(x3)
        y3 = float(y3)
        x12 = (x1 - x2)**2
        y12 =(y1 - y2)**2
        length12 = math.sqrt(x12+y12)

        x23 = (x2 - x3)**2
        y23 = (y2 - y3)**2
        length23 = math.sqrt(x23+y23)

        x13 = (x1 - x3)**2
        y13 = (y1 - y3)**2

        length13 = math.sqrt(x13+y13)

        term = (length13*length13 - length12*length12 - length23*length23) / (-2.0 * length12 * length23)

        if (term < -1):
            term = -1


        if (term > 1):
            term = 1

        angle = math.pi - math.acos(term);

        return math.degrees(angle)
    #
    def get_edge(x):
        for edge in edges:
            if (edge[0] == x):
                return edge
    def get_angle(x,y):

        edge1 = get_edge(x)
        edge2 = get_edge(y)
        if xnodes[edge1[1]] != xnodes[edge2[1]] and xnodes[edge1[1]] != xnodes[edge2[2]]:
            node1 = xnodes[edge1[1]]
            node2 = xnodes[edge1[2]]
        else:
            node1 = xnodes[edge1[2]]
            node2 = xnodes[edge1[1]]

        node3 = xnodes[edge2[1]]
        if node3 == node1 or node3 == node2:
            node3 = xnodes[edge2[2]]
    ##    print node1, node2, node3
        return angle(node1[1],node1[2],node2[1],node2[2],node3[1],node3[2])

    def successor(edge,edgeSuccessors, examined=[]):
        '''returns adjaccent edges to argument edge which are not in examined list'''
        successors = []
        #print 'ex',edge,edgeSuccessors[edge[0]]
        #for edge2 in edgeSuccessors[edge[0]]:
        #for edge2 in edges:
            #if edge == edge2:
                #continue
            #if edge[2] in edge2[1:3]:
                #if edge2[0] not in examined:
    ##                print 'succ', edge, edge2
                    #if edge[2]==edge2[1]:
                        #successors.append([edge2[0], edge2[1], edge2[2], edge2[3], edge2[4], edge2[5]])
                    #else:
                        #successors.append([edge2[0], edge2[2], edge2[1], edge2[3], edge2[4], edge2[5]])
        successors2=[]
        for edge2 in edgeSuccessors[edge[0]]:
        
            if edge == edge2:
                continue
            if edge[2] in edge2[1:3] :
                if edge2[0] not in examined:
    #                print 'succ', edge, edge2
                    if edge[2]==edge2[1]:
                        successors2.append([edge2[0], edge2[1], edge2[2], edge2[3], edge2[4], edge2[5]])
                    else:
                        successors2.append([edge2[0], edge2[2], edge2[1], edge2[3], edge2[4], edge2[5]])
        #if successors<>successors2:
            #print 'exception', edge, successors, successors2
        return successors2

    def expandSegment(edge, examined = [], result = [], buf=[], turns30 = []):
        examined.append(edge[0])
        #print 'result', result, 'examined', examined
        #print 'successors', edge, successor(edge, edgeSuccessors,examined)
        successors=successor(edge,edgeSuccessors, examined)
        if len(successors)==0:
            #deadend, end segment
            result.append([edge])
        for succ in successors:
            
            #print 'angle',edge, succ, angle(xnodes[edge[1]][1], xnodes[edge[1]][2], xnodes[edge[2]][1], xnodes[edge[2]][2], xnodes[succ[2]][1], xnodes[succ[2]][2])
            if succ not in examined and angle(xnodes[edge[1]][1], xnodes[edge[1]][2], xnodes[edge[2]][1], xnodes[edge[2]][2], xnodes[succ[2]][1], xnodes[succ[2]][2]) < 30:
                #print 'not_turn', edge, succ
                buf.append([edge,succ])
                #print 'buf', buf
                
                expandSegment(succ, examined, result,buf,turns30)
            elif (angle(xnodes[edge[1]][1], xnodes[edge[1]][2], xnodes[edge[2]][1], xnodes[edge[2]][2], xnodes[succ[2]][1], xnodes[succ[2]][2]) >= 30) and succ not in examined:
                #print 'turn', edge, succ, isTurn(turns,succ[0])
                #print 'tbuf', buf
                result.append([edge,succ])
                #turns30.append(succ[0])
        return result, buf, turns30
    
    def route(input, start, end, output=[]):
        #print 'start', start, 'end', end
        if start==end:
            #print 'start==end'
            #print 'output', output
            return output
        else:
            for pred in input:
                #print 'pred', pred, start, end
                if pred[1]==end:
                    # Songwei - input is buff. In buff, each element is [edge, succ], i.e., pred is [edge, succ]
                    predecessor=pred[0] #Songwei - pred[0]: edge
            output.append(predecessor)
            route(input,start,predecessor,output)
        #Songwei - segment I am looking for is output here, each element in segment (i.e., output) is predecessor (i.e., an edge), and e[4] I am looking for should be edge[4]
        #output.reverse()
        return output

    edges[:]=[e for e in edges if e[5]!='runway']    

    xnodes={}
    for node in nodes:
        xnodes[node[0]] = node
    xedges={}
    for edge in edges:
        xedges[edge[0]] = edge

 
    landmark_edges = []
    




    routes = []
    lengths = []

    
    #edge0x = [edgex[0], edgex[2], edgex[1], edgex[3], edgex[4], edgex[5]]
    #edge1x=xedges['1922']
    #routes0 = route(straight(edge0x,examined = [], result = []), edge0x, output=[[edge0x]])
    #print 'edge0', edge0x
    #print 'routes0', routes0
    
    #check for turn
    if predecessorNode != None:
        #print 'angle', predecessorNode,startingEdge, angle(xnodes[predecessorNode][1], xnodes[predecessorNode][2], xnodes[startingEdge[1]][1], xnodes[startingEdge[1]][2], xnodes[startingEdge[2]][1], xnodes[startingEdge[2]][2])
        if angle(xnodes[predecessorNode][1], xnodes[predecessorNode][2], xnodes[startingEdge[1]][1], xnodes[startingEdge[1]][2], xnodes[startingEdge[2]][1], xnodes[startingEdge[2]][2]) >= 30:
            #segments,buff,turns30=expandSegment(startingEdge,examined = [], result = [],buf=[startingEdge], turns30=[])
            return [[startingEdge]],[startingEdge[0]]
    segments,buff,turns30=expandSegment(startingEdge,examined = [], result = [],buf=[startingEdge], turns30=[])
    #Songwei - buff: straight, segments: turning. This is why buff is used below to generate reversed_segments
    #check if this is a deadend gate
    if len(segments)==0 and startingEdge[5]=='gate':
        #print 'xxx'
        return [[startingEdge]],turns30    
    #print 'straight', segments
    #print 'buff', buff
    #for segment in segments:
        #print segment, segment[0], segment[-1], sum([float(e[4]) for e in segment])
    reversed_segments =[]
    for seg in segments:
        s=route(buff,startingEdge,seg[0],output=[seg[0]])
        # Songwei - buff: input, startingEdge: start (an edge), seg[0]: end (an edge)
        s.reverse()
        if s not in reversed_segments:
            reversed_segments.append(s)
        #print 'x',edgex, seg[0], s
        #print 'starts', s[0], 'ends', s[-1], 'len', sum([float(e[4]) for e in s])
    return reversed_segments, turns30

def writeSegments_kqpptw(nodes,edges,turns,edgeSuccessors):
    xnodes={}
    for node in nodes:
        xnodes[node[0]] = node

    def get_successor(edge,edges):
        return [e for e in edges if (edge[1] in e[1:3] or edge[2] in e[1:3]) and e[0]!=edge[0]]


    def angle(x1,y1,x2,y2,x3,y3):
    ##    print x1,y1,x2,y2,x3,y3
        angle = 0.0
        x1 = float(x1)
        x2 = float(x2)
        y1 = float(y1)
        y2 = float(y2)
        x3 = float(x3)
        y3 = float(y3)
        x12 = (x1 - x2)**2
        y12 =(y1 - y2)**2
        length12 = math.sqrt(x12+y12)

        x23 = (x2 - x3)**2
        y23 = (y2 - y3)**2
        length23 = math.sqrt(x23+y23)

        x13 = (x1 - x3)**2
        y13 = (y1 - y3)**2

        length13 = math.sqrt(x13+y13)

        term = (length13*length13 - length12*length12 - length23*length23) / (-2.0 * length12 * length23)

        if (term < -1):
            term = -1


        if (term > 1):
            term = 1

        angle = math.pi - math.acos(term);

        return math.degrees(angle)
    def get_angle(x,y):

        edge1 = get_edge(x)
        edge2 = get_edge(y)
        #print 'edge', edge1, edge2
        if xnodes[edge1[1]] != xnodes[edge2[1]] and xnodes[edge1[1]] != xnodes[edge2[2]]:
            node1 = xnodes[edge1[1]]
            node2 = xnodes[edge1[2]]
        else:
            node1 = xnodes[edge1[2]]
            node2 = xnodes[edge1[1]]

        node3 = xnodes[edge2[1]]
        if node3 == node1 or node3 == node2:
            node3 = xnodes[edge2[2]]
        #print node1, node2, node3
        return angle(node1[1],node1[2],node2[1],node2[2],node3[1],node3[2])
    def get_edge(x):
        for edge in edges:
            if (edge[0] == x):
                return edge
    def successor(edge,edgeSuccessors, examined=[]):
        '''returns adjaccent edges to argument edge which are not in examined list'''
        successors = []
        #print 'ex',edge,edgeSuccessors[edge[0]]
        #for edge2 in edgeSuccessors[edge[0]]:
        #for edge2 in edges:
            #if edge == edge2:
                #continue
            #if edge[2] in edge2[1:3]:
                #if edge2[0] not in examined:
    ##                print 'succ', edge, edge2
                    #if edge[2]==edge2[1]:
                        #successors.append([edge2[0], edge2[1], edge2[2], edge2[3], edge2[4], edge2[5]])
                    #else:
                        #successors.append([edge2[0], edge2[2], edge2[1], edge2[3], edge2[4], edge2[5]])
        successors2=[]
        for edge2 in edgeSuccessors[edge[0]]:
        
            if edge == edge2:
                continue
            if edge[2] in edge2[1:3] :
                if edge2[0] not in examined:
    #                print 'succ', edge, edge2
                    if edge[2]==edge2[1]:
                        successors2.append([edge2[0], edge2[1], edge2[2], edge2[3], edge2[4], edge2[5]])
                    else:
                        successors2.append([edge2[0], edge2[2], edge2[1], edge2[3], edge2[4], edge2[5]])
        #if successors<>successors2:
            #print 'exception', edge, successors, successors2
        return successors2
    segmentsDict={}
    for edge1 in edges:
        for edge2 in edges:
            if edge1 == edge2:
                continue
            if edge1[1] in edge2[1:3] or edge1[2] in edge2[1:3]:
                if get_angle(edge1[0], edge2[0]) >=30:
                    #print 'angle',edge1[0],edge2[0]
                    for succ in successor(edge1,edgeSuccessors):
                        predNode=edge1[1]
                        #print 'succ', succ, predNode
                        segments1,trns1=expandSegments_kqpptw(succ,nodes,edges,predNode,edgeSuccessors)
                        segmentsDict[succ[1]+'x'+succ[2]+'x'+predNode]=(segments1,trns1)
                    edgex1=[edge1[0], edge1[2], edge1[1], edge1[3], edge1[4], edge1[5]]
                    for succ in successor(edgex1,edgeSuccessors):
                        predNode=edgex1[1]
                        #print 'succ2', succ, predNode
                        segments2,trns2=expandSegments_kqpptw(succ,nodes,edges,predNode,edgeSuccessors)
                        segmentsDict[succ[1]+'x'+succ[2]+'x'+predNode]=(segments2,trns2)
                    for succ in successor(edge2,edgeSuccessors):
                        predNode=edge2[1]
                        #print 'succ3', succ, predNode
                        segments3,trns3=expandSegments_kqpptw(succ,nodes,edges,predNode,edgeSuccessors)
                        segmentsDict[succ[1]+'x'+succ[2]+'x'+predNode]=(segments3,trns3)
                    edgex2=[edge2[0], edge2[2], edge2[1], edge2[3], edge2[4], edge2[5]]
                    for succ in successor(edgex2,edgeSuccessors):
                        predNode=edgex2[1]
                        #print 'succ4', succ, predNode
                        segments4,trns4=expandSegments_kqpptw(succ,nodes,edges,predNode,edgeSuccessors) 
                        segmentsDict[succ[1]+'x'+succ[2]+'x'+predNode]=(segments4,trns4)
                        
    for i,edge in enumerate(edges):
        segments=[]
        #print i, 'of', len(edges), len(segments), edge
        if edge[5] =='gate':
            predNode=None
            segments1,trns1=expandSegments_kqpptw(edge,nodes,edges,predNode,edgeSuccessors)
            edgex=[edge[0], edge[2], edge[1], edge[3], edge[4], edge[5]]
            segments2,trns2=expandSegments_kqpptw(edgex,nodes,edges,predNode,edgeSuccessors)
            segments.extend(segments1)
            segments.extend(segments2)
            segmentsDict[edge[0]]={}
            #by forward node, i.e. 2nd one
            segmentsDict[edge[1]+'x'+edge[2]+'x'+str(predNode)]=(segments1,trns1)

            segmentsDict[edgex[1]+'x'+edgex[2]+'x'+str(predNode)]=(segments2,trns2)

                
    #print 'segments', len(segmentsDict)
    return segmentsDict