# General interface/pseudocode

General questions

- do we want outputs as a named dictionary, a list, other?
- what are we using to speak to the DB? I am assuming it can be passed as an arg rather than re-validating for each query.

## Get info about ticket sender `getSender`

### Inputs

- **`swconn`** a connection to SpiceWorks
- **`ticket`** the ticket ID (`tickets.id`) *OR* **`user`** the user ID (`ticket.reported_by_id`) **Which one do we want?**

### Outputs

- email (from `users.email`)
- name (from (`users.first_name` + `users_last.name`)) **This field is only filled out for "real" users (ProUser type) - what do we want to do with email-only users (EndUser type)?**
- phone number (from `users.office_phone` or `users.cell_phone`) **This field is almost always empty in SW - do we actually want it?**

## Get ticket content `getTicket`

### Inputs

- **`swconn`** a connection to SpiceWorks
- **`ticket`** the ticket ID (`tickets.id`)

### Outputs

- ticket id (from `tickets.id`) note: this is also one of the inputs! Returned for validation
- summary (from `tickets.summary`)
- description (from `tickets.description`) **potentially look to do some text cleaning if there is an encoding issue**
- Time ticket of last
    - Created (from `tickets.created_at`)
    - Closed (from `tickets.closed_at`)
- Created by, but by the email of that user (from `users.email where users.id = tickets.created_by`)
- c_spe (from `tickets.c_spe`)
- c_department (from `tickets.c_department`)

## Get all ticket comments into one big HTML string

- Do we want this to actually run as part of the previous function (as another output of the same call)?

### Inputs

- **`swconn`** a connection to SpiceWorks
- **`ticket`** the ticket ID (`tickets.id`)

### Outputs

- comment chunk built from `comments` in the following format

        <p><br /></p> 
        <p>created_at time created_by person 1 email: content of body..</p> 
        <p>created_at time created_by person 2 email: content of body..</p> 
        <p>Find the attachments to this ticket: C:\\Program Files (x86)\\Spiceworks\\data\\uploads\\Ticket\\ticket_id<br /></p>'

  content extracted from
    - person email: `users.email where users.id = comments.created_by`
    - timestamp: `comments.created_at`
    - body: `comments.body` **May need a bit of HTML transform (e.g. `<br>` lines)**
    - attachments: `C:\\Program Files (x86)\\Spiceworks\\data\\uploads\\Ticket\\`*`ticket_id`*`\\`_`attachment_name`_
  collated from `comments where comments.ticket_id = tickets.id`

Notes:

- A raw example from osTicket would really help here (e.g. formatting of timestamp)
- Do we want to keep auto-comments "Assigned to...", "Ticket closed/reopened", "Attachment:", etc.?
- Do we want links to individual attachments or just the overall folder? In either case we may want to put the Spiceworks data folder on a share, so it can be accessed without remoting into the Spicewoks server. We can either mount Tickets or copy it to an already shared drive. No idea how to do it in Windows.
