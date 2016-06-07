## Database-access-update-feature
MySQL database easy access/update feature implemented with Python and Flask. <br /> 
Allows adding, removal, updating and listing of the content of a database's tables.

##### Used:
Flask - web application <br />
peewee - easy and small ORM

##### Files:
api.py - routes and routines <br /> 
app.py - db hook <br /> 
main.py - run routine <br /> 
models.py - database models for object-relational mapping <br /> 
templates (folder) - HTML templates for rendering

##### Models.py
To gerenerate models.py file from an existing databse use pwiz:<br /> 
$ python -m pwiz -e postgresql my_db > models.py

##### To run:
$ python main.py

##### Screenshots:
![Alt text](/../screenshots/Index_page.png "Index page")
![Alt text](/../screenshots/List_devicerules.png "List device rules")
![Alt text](/../screenshots/Add_device.png "Add device")
![Alt text](/../screenshots/Remove_device.png "Remove device")
