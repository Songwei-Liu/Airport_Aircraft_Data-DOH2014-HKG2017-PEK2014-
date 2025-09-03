# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 15:18:18 2021

@author: Lilla Beke

Notes:
    Dominated costs can be included in the speed profile graph by modifying
    this file. 
    Function read_in_graph reads in a speed profile graph with ten or twenty 
    parallel speed profiles with non-dominated costs if the file is found. In 
    the exception it uses extract_basic_segment_based_graph to generate the
    graph. 
    The function extract_basic_segment_based_graph should be modified and a 
    new empty folder specified in folder_specifier with the key 'graph_data' to
    generate a new graph.
    I don't know to include speed profiles that are not in the database, 
    but I think it should be done in place of get_segment_info, 
    or in get_segment_info.
"""

import networkx as nx
from landmarks_kqpptw import expandSegments_kqpptw
from database import calculateEdgeTimes
from folder_specifier import get_folder


def read_in_graph(G_layout, segments_dict, airport_edges, airport_nodes,\
                  edge_successors, dbases, no_speed_profiles, airportInstance):
    """
    Tries to read in two speed profile graphs, one for medium and one for 
    heavy aircraft. If they are not in the specified folder, they are
    regenerated and saved.
    Also finds the highest value cost component to use later in scaling 
    penalties.
    """
    try:
        G_seg_base_H = nx.read_gpickle(get_folder('graph_data') + "/norm_" + \
                                       airportInstance + "_basic_heavy.gpickle")
        f = open(get_folder('graph_data') + airportInstance + "ma_heavy.txt")
        f_lines = f.readlines()
        ma_H = float(f_lines[0].strip())
        print('heavy read in from ', get_folder('graph_data'))
    except:
        G_seg_base_H, ma_H = extract_basic_segment_based_graph(G_layout, segments_dict,\
                                                               airport_edges, airport_nodes,\
                            edge_successors,'heavy',dbases,no_speed_profiles)
        nx.write_gpickle(G_seg_base_H, get_folder('graph_data') + "/norm_" +\
                         airportInstance + "_basic_heavy.gpickle")
        f = open(get_folder('graph_data') + airportInstance + "ma_heavy.txt", "w")
        f.write(str(ma_H))
        f.close()
        print('basic graph saved, heavy')
        
    try:
        G_seg_base_M = nx.read_gpickle(get_folder('graph_data') + "/norm_" +\
                                       airportInstance + "_basic_medium.gpickle")
        f = open(get_folder('graph_data')+airportInstance + "ma_medium.txt")
        f_lines = f.readlines()
        ma_M = float(f_lines[0].strip())
        print('medium read in')
    except:
        G_seg_base_M, ma_M = extract_basic_segment_based_graph(G_layout, segments_dict,\
                                                               airport_edges, airport_nodes,\
                            edge_successors, 'medium', dbases, no_speed_profiles)
        nx.write_gpickle(G_seg_base_M, get_folder('graph_data') + "/norm_" +\
                         airportInstance + "_basic_medium.gpickle")
        f = open(get_folder('graph_data') + airportInstance + "ma_medium.txt", "w")
        f.write(str(ma_M))
        f.close()
        print('basic graph saved, medium')
    
    return G_seg_base_H, ma_H, G_seg_base_M, ma_M


# building a graph that contains all information about all possible segments
# that are straight or turning. Holding segments are not included here.
def extract_basic_segment_based_graph(G_layout, segments_dict, airport_edges, \
                                      airport_nodes, edge_successors, weight_category, \
                                      dbases, no_speed_profiles, verbose = False):
    """
    Building a graph (G_segments) that contains all information about all segments
    needed for routing. The general version of the graph is generated here for
    either weight category, that does not include breakaway and holding speed profiles.
    Those are included by the adjust_segments function before routing each aircraft.
    All possible segments are listed by going through each edge of G_layout and 
    checking each possible predecessor node.
    For each segment the characteristics of the speed profiles from the database
    (dbases) are saved in dictionaries for each predecessor, as edge attributes.
    The edge attributes in G_segments are:
        c: cost vectors for each possible predecessor
        t: edge times for each possible predecessor
        last: last node of segment for each possible predecessor 
            (can be different), to use as predecessor for sequential speed profile
    """
    G_segments = nx.DiGraph()
    ma = 0
    for edge in G_layout.edges():
        current_edge = getEdge(edge[0],edge[1], airport_edges)
        current_edge = [current_edge[0], edge[0], edge[1], current_edge[3], current_edge[4], current_edge[5]]
        neighbors = list(G_layout.neighbors(edge[0]))
        neighbors.remove(edge[1])
        for predecessor in neighbors:
            if current_edge[1]+'x'+current_edge[2]+'x'+str(predecessor) in segments_dict:
                segments, turns30 = segments_dict[current_edge[1] + 'x' +\
                                                 current_edge[2] + 'x' + str(predecessor)]
            else:
                segments, turns30 = expandSegments_kqpptw(current_edge, airport_nodes,\
                                                       airport_edges, predecessor,\
                                                           edge_successors)
            for segment in segments:
                initial_v, end_v, segmentLen, segment_type, dbEntry, successor,\
                                    predNode = get_segment_info(segment, turns30, \
                                                        edge[1],edge[0],\
                                                        weight_category, dbases,\
                                                        current_edge)
                
                objSeg, _, _, _, edgeTimes = \
                        calculateEdgeTimes(0, [0,initial_v,end_v,segmentLen,segment_type,0],
                                           dbEntry,weight_category,segment,G_layout,no_speed_profiles)
                
                selectedObjSeg = objSeg
                
                for iobj, objective in enumerate(selectedObjSeg):
                    costs = (objective[0], objective[1]) 
                    for comp in costs:
                        if ma < comp:
                            ma = comp
                    times = dict((k, v[iobj]) for k, v in edgeTimes.items())
                    key = predecessor 
                    
                        
                    if not G_segments.has_edge(edge[0],successor) or G_segments[edge[0]][successor]=={}:
                        cost_dict = {}
                        cost_dict[key] = [costs]
                        et_dict = {}
                        et_dict[key] = [times]
                        last_dict = {}
                        last_dict[key] = [segment[-1][1]]
                        G_segments.add_edge(edge[0],successor,c=cost_dict,t=et_dict,last=last_dict)
                        if verbose:
                            print('added',edge[0],successor,key,cost_dict )
                        
                        
                    else: 
                        cost_dict = G_segments[edge[0]][successor]['c']
                        et_dict = G_segments[edge[0]][successor]['t']
                        last_dict = G_segments[edge[0]][successor]['last']
                        if key in cost_dict :
                            if costs not in cost_dict[(key)]:
                                cost_dict[key].append(costs)
                                et_dict[key].append(times)
                                last_dict[key].append(segment[-1][1] )
                                if verbose:
                                    print('added', edge[0], successor, key, cost_dict )
                        else:
                            cost_dict[key] = [costs]
                            et_dict[key] = [times]
                            last_dict[key] = [segment[-1][1]]
                        G_segments[edge[0]][successor]['c'] = cost_dict
                        G_segments[edge[0]][successor]['t'] = et_dict
                        if verbose:
                            print('added',edge[0], successor, key, cost_dict )
                        
    return G_segments, ma


def get_segment_info(segment, turns30, successorNode, end_of_decoded_path, \
                     weight_category, dbases, current_edge, start_node = None,\
                         end_node = None, acft_type = None):   
    """
    Get the speed profile data from the database, only aircraft specific if 
    start_node, end_node and acft_type is specified.
    Otherwise breakaway and holding segments are not identified, as needed for
    the general speed profile graph.
    """
    if len(segment) > 1:
        if segment[-1][1] not in segment[-2][1:3]: 
            successor = segment[-1][1]
            predNode = segment[-1][2]
        else:
            successor = segment[-1][2]
            predNode = segment[-1][1]
    else:
        successor = successorNode
        predNode = end_of_decoded_path
    
    segmentLen = float(sum([float(e[4]) for e in segment]))
    
    if end_of_decoded_path == start_node and acft_type == 'departure':
        #breakaway if departure
        initial_v = 0
        segment_type = 1
        end_v=5.14
        dbase=dbases[weight_category]['breakaway']
        try:
            dbEntry=dbase[round(segmentLen)]

        except KeyError:
            dbEntry=[0,0,0,0,0,0,0,0,0,0]
            segment_type=2
            initial_v=5.14
            
    elif len(segment)==1 and segment[0][0] in turns30:
        
        initial_v=5.14
        segment_type=2
        end_v=5.14
        dbEntry=[0,0,0,0,0,0,0,0,0,0]
        
    elif successor == end_node:
       
        initial_v=5.14
        segment_type=3
        end_v=0  
        dbase=dbases[weight_category]['hold']
        
        try:
            dbEntry=dbase[round(segmentLen)] 
            
        except KeyError:
            dbEntry=[0,0,0,0,0,0,0,0,0,0]
            segment_type=2
           
    else:
        initial_v=5.14
        segment_type=1
        end_v=5.14  
        dbase=dbases[weight_category]['straight']
        try:
            dbEntry=dbase[round(segmentLen)]
        except KeyError:
            segment_type=2
            dbEntry=[0,0,0,0,0,0,0,0,0,0]

    return initial_v, end_v, segmentLen, segment_type, dbEntry, successor, predNode

    
def getEdge(start_node,end_node,edges):
    """ 
    Find the rest of the edge data based on start node and end node.
    """
    e = None
    for edge in edges:
        if start_node in edge[1:3] and end_node in edge[1:3]:
            e = edge
            break
    return e