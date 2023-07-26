# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 18:48:58 2023

@author: PCOGNIGN
"""

import sqlite3

def get_spiceworks():
    """
    Connects to the SpiceWorks SQLite database

    Parameters
    ----------
    None

    Returns
    -------
    sqlite3.Connection object
    """
    if 'SWlocation' not in locals() and 'SWlocation' not in globals() :
        try:
            config = open('SWlocation.txt')
            SWlocation = config.readline()
            config.close()
        except FileNotFoundError():
            print("Please create a SWlocation.txt file with the path to the Spiceworks database")
    return sqlite3.connect(SWlocation)
