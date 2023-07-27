# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 18:48:58 2023

@author: PCOGNIGN
"""

import sqlite3
from os import access, R_OK
from os.path import isfile

def get_spiceworks(location = None):
    """
    Connects to the SpiceWorks SQLite database

    Parameters
    ----------
    None

    Returns
    -------
    sqlite3.Connection object
    """
    if location is None:
        try:
            config = open('SWlocation.txt')
            location = config.readline()
            config.close()
        except FileNotFoundError():
            print("Please pass the path to the Spiceworks database or create a SWlocation.txt file")
    # =============================================================================
    #     Check that the location exists and is a readable file, 
    #     otherwise sqlite3 creates one in the current directory 
    #     which is pretty annoying. Allow the special case ":memory:"
    # =============================================================================
    if location == ':memory:' or (isfile(location) and access(location, R_OK)):
        return sqlite3.connect(location)
    print('The location %s is not a valid file' % location)
