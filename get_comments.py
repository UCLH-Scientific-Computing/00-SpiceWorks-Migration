# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 17:49:46 2023

@author: PCOGNIGN
"""

from get_spiceworks import get_spiceworks
from make_html import make_html_comment

def get_comments(id):
    """
    Retrieves and collates all comments given the ticket id

    Parameters
    ----------
    id : int
        The ticket id.

    Returns
    -------
    dict of {str : str}    
        A dictionary of comment thread info derived from database fields:
            id: the ticket id
            body: an HTML string of all the comments collated together
    """
    con = get_spiceworks()
    cursor = con.cursor()
    query = 'SELECT comments.id, ticket_id, comments.body, comments.created_at, users.email, attachment_name FROM comments JOIN users on comments.created_by = users.id WHERE ticket_id = :id ORDER BY comments.id DESC'
    result = cursor.execute(query, {'id': id})
    comments = [ make_html_comment(row) for row in result.fetchall() ]
    con.close()
    return '<hr>'.join(comments)
