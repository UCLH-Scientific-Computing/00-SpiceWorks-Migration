# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 17:49:46 2023

@author: PCOGNIGN
"""

from get_spiceworks import get_spiceworks

def get_ticket(id):
    """
    Retrieves ticket information given the ticket id

    Parameters
    ----------
    id : int
        The ticket id.

    Returns
    -------
    dict of {str : str}    
        A dictionary of ticket info derived from database fields:
            ticket id (from `tickets.id`) note: this is also one of the inputs! Returned for validation
            summary (from `tickets.summary`)
            description (from `tickets.description`) **potentially look to do some text cleaning if there is an encoding issue**
            created_at (from `tickets.created_at`)
            closed_at (from `tickets.closed_at`)
            created_by, but by the email of that user (from `users.email where users.id = tickets.created_by`)
            spe (from `tickets.c_spe`)
            department (from `tickets.c_department`)
    """
    con = get_spiceworks()
    cursor = con.cursor()
    query = 'SELECT tickets.id, summary, description, tickets.created_at, closed_at, users.email, c_spe, c_department FROM tickets JOIN users on tickets.created_by = users.id WHERE tickets.id = :id'
    cursor.execute(query, {'id': id})
    result = cursor.fetchone()
    return dict(zip(['id', 'summary', 'description', 'created_at', 'closed_at', 'created_by', 'spe', 'department'], result))
