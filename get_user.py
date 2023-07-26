# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 17:49:46 2023

@author: PCOGNIGN
"""

import sqlite3

def get_user(id):
    """
    Retrieves user information given the user id

    Parameters
    ----------
    id : int
        The user id.

    Returns
    -------
    dict of {str : str}    
        A dictionary of user info derived from database fields:
            id: the user id
            email: the user email
            name: the user name, concatenating first_name and last_name
            phone: the user phone number, concatenating office_phone and mobile_phone
    """
    con = sqlite3.connect("M:\Projects\Ticketing\Spiceworks\spiceworks_prod.db")
    cursor = con.cursor()
    query = 'SELECT id, email, TRIM(first_name || " " || last_name), TRIM(office_phone || " " || cell_phone) FROM users WHERE id = :id'
    cursor.execute(query, {'id': id})
    result = cursor.fetchone()
    return dict(zip(['id', 'email', 'name', 'phone'], result))
    
    
def get_user_fields(id, fields = ["id"]):
    """
    Retrieves user information given the user id

    Parameters
    ----------
    id : int
        The user id.
    fields : list of string, default ["id"]
        Which fields are requested from the user table

    Returns
    -------
    dict of {str : str}    
        A dictionary of the fields requested in the param "fields" with the returned value
    """
    con = sqlite3.connect("M:\Projects\Ticketing\Spiceworks\spiceworks_prod.db")
    cursor = con.cursor()
    query = 'SELECT %s FROM users WHERE id = :id' % ', '.join(fields)
    cursor.execute(query, {'id': id})
    result = cursor.fetchone()
    return dict(zip(fields, result))
