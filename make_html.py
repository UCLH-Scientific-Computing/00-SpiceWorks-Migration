# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 12:05:30 2023

@author: PCOGNIGN
"""

from re import sub

def make_html_comment(row) :
    """
    Format all Spiceworks comments from one ticket into a single HTML chunk
    containing comment author (email), timestamp and body text

    Parameters
    ----------
    row : tuple(<int>, <int>, <string>, <string>, <string>, <string>|None)
        The row data as extracted inside get_comments, containing:
            id: the comment id
            ticket_id: the id of the ticket this comment is for
            body: the text of the comment
            created_at: the timestamp of comment submission
            email: the email of the comment author
            attachment: the name of an attached file, if any, or None.

    Returns
    -------
    str
        An HTML string with each comment in reverse submission order, with 
        an H3 header for the author email and timestamp, the (roughly HTML-ified)
        body text, and the name of the attachment, if any.

    """
    body = '<h3><code>%s</code> on %s:</h3><p>%s</p>' % (row[4], row[3], row[2])
    if row[5] is not None:
        body += '<p>'
        if row[2] != 'Attachment:':
            body += 'Attachment:</p><p>'
        body += '<em>%s</em></p>' % row[5] 
    return sub(r'(\r)?\n', r'<br>', body)
