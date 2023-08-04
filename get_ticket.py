# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 17:49:46 2023

@author: PCOGNIGN
"""

from get_spiceworks import get_spiceworks
from re import sub

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
            id (from `tickets.id`)
            summary (from `tickets.summary`)
            description (from `tickets.description`) **potentially look to do some text cleaning if there is an encoding issue**
            created_at (from `tickets.created_at`)
            closed_at (from `tickets.closed_at`)
            created_by, but by the email of that user (from `users.email where users.id = tickets.created_by`)
            assigned_to, but by the email of that user (from `users.email where users.id = tickets.assigned_to`)
            spe (from `tickets.c_spe`)
            department (from `tickets.c_department`)
        If the input id did not yield a ticket, returns an empty dict.
    """
    con = get_spiceworks()
    cursor = con.cursor()
    query = 'SELECT tickets.id, summary, description, tickets.created_at, closed_at, creator.email, staff.email, c_spe, c_department FROM tickets LEFT JOIN users creator ON tickets.created_by = creator.id LEFT JOIN users staff ON tickets.assigned_to = staff.id WHERE tickets.id = :id'
    cursor.execute(query, {'id': id})
    result = list(cursor.fetchone())
    result[2] = sub(r'(\r)?\n', r'<br>', result[2])
    con.close()
    if result is None:
        return {}
    return dict(zip(['id', 'summary', 'description', 'created_at', 'closed_at', 'created_by', 'assigned_to', 'spe', 'department'], result))
