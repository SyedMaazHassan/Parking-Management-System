# Parking-Management-System

allows users to book parking places after creating their account.

MAIN PAGES:

1) main_page (opening pages, having login & signup options)
2) form_signup (a form based page which lets users to register)
3) form_login (a form based page to login into the system)
4) parking_map (our main software page which has parking map & booking options)

USER CAN:

1) Book any available slots in the given parking map (map update on real time)
2) Bring out their parked vehicle. (booked slots will be available for others after this action)
3) Provide feedback
4) Logout

TECHNOLOGY USED:

*it's a web application

FRONTEND => html, css, javascript(a little bit)
BACKEND => python 3 (with its popular web framework DJANGO 3.0.3)

DATABASE:

SQLite3 database is used to store, update, and delete the records (a/c to the need)

TABLES in DATABASE:

1) USERS (having all the user data about registered users)
2) CARS (having all slots with boolean value of BOOKED or NOT BOOKED)
3) AH (having data about the users that logins at the moment)
4) HISTORY (having all the history, who and when a user books which slots)
5) BOOK (having slots numbers with person_id who books that slot)
6) FB (having all feedbacks alongwith the person name who provide the feedback)

DESIGN & DEVELOPED BY SYED MAAZ HASSAN

