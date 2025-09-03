#26.05.2016

def gm_parser(gmfile,gmfile_angles):
    """parsing tool from GM files to python lists"""
    
    file = open(gmfile,"r")

    nodes = []
    edges = []
    nodes_started = 0
    edges_started = 0
    for line in file:
        if '%SECTION%1%;Nodes;' in line:
            nodes_started = 1
        if nodes_started ==1 and '%' not in line:
            buf = line.split(';')
            #print buf[1:-1]
            nodes.append(buf[1:-1])
        if '%SECTION%1%;Edges;' in line:
            nodes_started = 0
            edges_started = 1
        if edges_started ==1 and '%' not in line:
            buf = line.split(';')
            #print buf[1:-1]
            edges.append(buf[1:-1])

    file2 = open(gmfile_angles,"r")
    angles = []
    for line in file2:
        if '#' not in line:
            buf = line.split(';')
            angles.append(buf[1:-1])
    return angles, nodes, edges


def gm_parser2(gmfile,gmfile_angles):
    """parsing tool from GM files to python lists"""
    file = open(gmfile,"r")

    nodes = []
    edges = []
    aircrafts = []
    nodes_started = 0
    edges_started = 0
    acft_started = 0
    for line in file:
        if '%SECTION%1%;Nodes;' in line:
            nodes_started = 1
            edges_started = 0
            acft_started = 0
        if nodes_started ==1 and '%' not in line:
            buf = line.split(';')
            #print buf[1:-1]
            nodes.append(buf[1:-1])
        if '%SECTION%1%;Edges;' in line:
            nodes_started = 0
            edges_started = 1
            acft_started = 0
        if edges_started ==1 and '%' not in line:
            buf = line.split(';')
            #print buf[1:-1]
            edges.append(buf[1:-1])
        if '%SECTION%1%;Aircraft;' in line:
            nodes_started = 0
            edges_started = 0
            acft_started = 1
        if acft_started ==1 and '%' not in line:
            buf = line.split(';')
            #print buf
            aircrafts.append([])
            for b in buf:
                
                if '[' in b:
                    b_split=b[1:-1].split(',')
                    aircrafts[-1].append(b_split)
                else:
                    if b != '':
                        
                        aircrafts[-1].append(b.replace('\n',''))
            #print buf[1:-1]
            #aircrafts.append(buf[1:-1])

    angles = []
    try:
        file2 = open(gmfile_angles,"r")
    
        for line in file2:
            if '#' not in line:
                buf = line.split(';')
                angles.append(buf[1:-1])
    except:
        pass

    return angles, nodes, edges, aircrafts