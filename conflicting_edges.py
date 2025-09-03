def readConflictingEdges(filename):
    conflicting_edges={}
    for i,line in enumerate(open(filename)):
        if i==0:
            continue
        buf=line[:-1].split(';')
        conflicting_edges[buf[0]]={}
        for edgeBuf in buf[1:]:
            buf2=edgeBuf.split(',')
            
            conflicting_edges[buf[0]][buf2[0]]=float(buf2[1])
    return conflicting_edges