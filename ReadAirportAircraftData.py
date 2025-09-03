"""
@author: Lilla Beke edited in 2021, Songwei Liu edited in 2025
"""

import networkx as nx
from airport_functions import read_in_graph
from conflicting_edges import readConflictingEdges
from folder_specifier import get_folder
from gm_parse import gm_parser, gm_parser2
from landmarks_kqpptw import writeSegments_kqpptw

def readDbase(filename):
    file=open(filename, "r")
    dbase={}
    
    for line in file:
        buf=line.split('\t')
        dbase[float(buf[0])]=[float(b) for b in buf[1:-1]]
        
    return dbase


def read_in_airport_data(airportInstance):
    """
    Reads in airport data from a folder.

    Parameters
    ----------
    airportInstance : str
        doh (small), hkg (medium), or pek (large)

    Returns
    -------
    nodes : nodes of airport layout
    edges : edges of airport layout
    dbases : where speed profile data is stored
    conflicting_edges : inforation about which edges are close enough so they are conflicting
    aircrafts : the data about the routing tasks (what aircraft, starting and end positions)
    """
    
    data_path = get_folder('data_path') # path to the data folder
    # directing to './main_data/data/'
    
    if airportInstance == "doh":
        _, nodes, edges = gm_parser(data_path + 'doh.txt', data_path + 'PEK5_angles.txt')
        # gm_parser: import nodes & edges via data_path+'doh.txt', and import angles via data_path+'PEK5_angles.txt' (not assigned to a variable)
        # Airport angle data of Doha and Hongkong are also saved in 'PEK5_angles.txt'

        _, _, _, aircrafts = gm_parser2(data_path + 'doh_all.acr', '')
        # gm_parser2:import aircraft via data_path+'doh_all.acr'

        dbases = {'medium': {'straight': readDbase(data_path + 'dbase_doh_medium.txt'),\
                             'breakaway': readDbase(data_path + 'dbase_doh_breakaway_medium.txt'),\
                                'hold': readDbase(data_path + 'dbase_doh_hold_medium.txt')}}
        dbases['heavy'] = {'straight': readDbase(data_path + 'dbase_doh_heavy.txt'), \
                           'breakaway': readDbase(data_path + 'dbase_doh_breakaway_heavy.txt'),\
                                'hold': readDbase(data_path + 'dbase_doh_hold_heavy.txt')} 
        conflicting_edges = readConflictingEdges(data_path + 'doh_conflicting_edges.txt')
        
    elif airportInstance[:3] == "hkg":
        _, nodes, edges = gm_parser(data_path + 'hkg_network_post.txt', data_path+'PEK5_angles.txt')
        # gm_parser: import nodes & edges via data_path+'hkg_network_post.txt', and import angles via data_path+'PEK5_angles.txt' (not assigned to a variable)

        if airportInstance == "hkg":
            _, _, _, aircrafts = gm_parser2(data_path + 'hkg_17_jan_2017.acr', '')
            # gm_parser2:import aircraft via data_path+'hkg_17_jan_2017.acr'
        else:
            _, _, _, aircrafts = gm_parser2(data_path + airportInstance + '.txt', '')
        
        dbases = {'medium': {'straight': readDbase(data_path + 'dbase_pek_medium.txt'),\
                             'breakaway': readDbase(data_path + 'dbase_hkg_breakaway_medium.txt'),\
                                'hold': readDbase(data_path + 'dbase_hkg2_hold_medium.txt')}}
        
        dbases['heavy'] = {'straight': readDbase(data_path + 'dbase_pek_heavy.txt'),\
                           'breakaway': readDbase(data_path + 'dbase_hkg_breakaway_heavy.txt'),\
                                'hold': readDbase(data_path + 'dbase_hkg_hold_heavy.txt')} 
        conflicting_edges = readConflictingEdges(data_path + 'hkg_conflicting_edges_post.txt')
        
    elif airportInstance == "pek":
        _, nodes, edges = gm_parser(data_path + 'pek5.txt',data_path+'PEK5_angles.txt')
        # gm_parser: import nodes & edges via data_path+'pek5.txt', and import angles via data_path+'PEK5_angles.txt' (not assigned to a variable)
        _, _, _, aircrafts = gm_parser2(data_path + 'pek_all.acr','')
        ## gm_parser2:import aircraft via data_path+'pek_all.acr'

        dbases = {'medium': {'straight': readDbase(data_path + 'dbase_pek_medium.txt'),\
                             'breakaway':readDbase(data_path + 'dbase_pek_breakaway_medium.txt'),\
                                 'hold':readDbase(data_path + 'dbase_pek_hold_medium.txt')}}
        dbases['heavy'] = {'straight': readDbase(data_path + 'dbase_pek_heavy.txt'),\
                           'breakaway':readDbase(data_path + 'dbase_pek_breakaway_heavy.txt'),\
                               'hold':readDbase(data_path + 'dbase_pek_hold_heavy.txt')} 
        conflicting_edges = readConflictingEdges(data_path + 'pek5_conflicting_edges.txt')
        
    return nodes, edges, dbases, conflicting_edges, aircrafts


def initialise_layout_graph(edges):
    """
    Build layout graph.

    Parameters
    ----------
    edges :  edges of airport layout.

    Returns
    -------
    G : NetworkX graph that represents the layout graph of the given airport.
    """

    G = nx.DiGraph()
    for edge in edges:
        if edge[5] != 'runway':
            G.add_edge(edge[1], edge[2], edge_id = edge[0], c = (float(edge[4]), 0),\
                        tw = [[0.0,float('inf')]], length = float(edge[4]))
            G.add_edge(edge[2], edge[1], edge_id = edge[0], c = (float(edge[4]), 0),\
                        tw = [[0.0,float('inf')]], length = float(edge[4]))
    return G


def build_edge_successors(edges):
    """
    Find neighbouring edges for each edge. 
    Used in later operations on the graphs associated with the airport.

    Parameters
    ----------
    edges : edges of airport layout.
    
    Returns
    -------
    edge_successors : dict
        Lists possible successor edges for each node in the airport.
    """
    edge_successors = {}
    for edge1 in edges:
        for edge2 in edges:
            if edge1 == edge2:
                continue
            if edge1[1] in edge2[1:3] or edge1[2] in edge2[1:3]:
                if edge1[0] in edge_successors:
                    edge_successors[edge1[0]].append(edge2)
                else:
                    edge_successors[edge1[0]]=[edge2]
    return edge_successors


# Songwei - Not used in this file but saved here as reference in case it is needed.
def adjust_all_time_windows_in_path(G,edges,path,conflicting_edges):
    """
    Update time windows to reflect occupation of edges by the last routed aircraft.

    Parameters
    ----------
    G : NetworkX graph
        Layout graph.
    edges : edges of the airport layout.
    path : list
        path describing the edges included in the current chosen trajectory.
    conflicting_edges : dict
        Edges conflicting with each edge in the layout.

    Returns
    -------
    G : NetworkX graph
        Layout graph with updated time windows.

    """
    xedges = {edge[0]:edge for edge in edges}
    conflicting_threshold = 60 #distance in m, -1 to turn off
    pathEdges=[e  for segment in path for e in list(segment[2]['et'].keys())]
    for segment in path:
        edgeTimes=segment[2]['et']
        for edgeId in edgeTimes:
            edgeTime=edgeTimes[edgeId][0]            
            #go through conflicting_edges and reserve edges that are nearer than threshold and not in path
            for edgeId2 in conflicting_edges[edgeId]:
                if conflicting_edges[edgeId][edgeId2]<=conflicting_threshold and edgeId2 not in pathEdges:
                    #reserving conflicting edge (edgeId2)
                    edge=xedges[edgeId2]
                    timeWindows=G[edge[1]][edge[2]]['tw']
                    G[edge[1]][edge[2]]['tw']=calculate_new_time_windows(timeWindows,edgeTime)
                    
            edge=xedges[edgeId]
            timeWindows=G[edge[1]][edge[2]]['tw']
            G[edge[1]][edge[2]]['tw']=calculate_new_time_windows(timeWindows,edgeTime)
    return G


def calculate_new_time_windows(timeWindows,edgeTime):
    """
    Calculate new time windows on a given edge given a new interval 
    of traversal (edgeTime) and the current time windows (timeWindows).

    Parameters
    ----------
    timeWindows : list of lists, where each sub list includes two floats
        List of time windows, that is intervals when the given edge is free.
    edgeTime : list (two floats)
        The time of occupation of the given edge by the last routed aircraft.

    Returns
    -------
    newTimeWindows : list of lists, where each sub list includes two floats
        Updated lists of time windows on given edge.

    """
    newTimeWindows = []
    for timeWindow in timeWindows:
        # if the edge traversal is within the timeWindow, 
        # the interval before and after are the new time windows.
        if edgeTime[0]>=timeWindow[0] and edgeTime[1]<=timeWindow[1]:
            newWindow1 = [timeWindow[0],edgeTime[0]]
            newWindow2 = [edgeTime[1],timeWindow[1]]
            newTimeWindows.append(newWindow1)
            newTimeWindows.append(newWindow2)
        else:
            newTimeWindows.append(timeWindow)
    #remove time windows shorter than 1 s
    for timeWindow in newTimeWindows:
        if (timeWindow[1]-timeWindow[0])<=1:
            newTimeWindows.remove(timeWindow)
    return newTimeWindows


if __name__ == "__main__":

    # user defined arguments
    airportInstance = 'doh' # options: 'doh', 'hkg', or 'pek'
    speed_profiles = 10     # how many speed profiles to include in speed prophile graph
    

    # load airport data
    airport_nodes, airport_edges, dbases, conflicting_edges, aircrafts = read_in_airport_data(airportInstance)
    aircrafts.sort(key=lambda x:int(float(x[4][0]))) # Songwei - sorting based on aircraft's start_time

    edges2 = [e for e in airport_edges if e[5] != 'runway']
    edge_successors = build_edge_successors(edges2)
    segment_dict = writeSegments_kqpptw(airport_nodes, edges2, [], edge_successors)
    
    # get the layout graph
    G_layout = initialise_layout_graph(airport_edges)
    
    # get the base of the speed profile graphs for both heavy and medium aircraft
    G_seg_base_H_all,ma_H, G_seg_base_M_all,ma_M = read_in_graph(G_layout,segment_dict, airport_edges,\
                                                                 airport_nodes, edge_successors, dbases,\
                                                                    speed_profiles, airportInstance)
