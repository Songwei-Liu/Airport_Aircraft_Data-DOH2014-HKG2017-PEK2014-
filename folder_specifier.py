# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 15:18:18 2021

@author: Lilla Beke

"""


def get_folder(key):
    """
    All paths are stored here that are used in any of the files.
    """
    
    main_path = "./main_data/"
    
    # airport layout data and aircraft sequence
    if key == 'data_path':
        return main_path+"data/"
    # hopcount data
    if key == 'data_path2':
        return main_path+'data2/'
    
    # the basic speed profile graph
    if key == 'graph_data':
        return main_path+"graph_data_4/"