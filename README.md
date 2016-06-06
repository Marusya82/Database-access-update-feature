# Database-access-update-feature
MySQL database easy access/update feature implemented with Python and Flask. Allows adding, removal, updating and listing of the content of a database's tables.

Used:
Flask - web application 
peewee - easy and small ORM

Files:
api.py - routes and routines
app.py - db hook
main.py - run routine
models.py - database models for object-relational mapping
templates (folder) - HTML templates for rendering

To gerenerate models.py file from an existing databse use pwiz (http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#pwiz):
python -m pwiz -e postgresql my_db > models.py

To run:
python main.py
