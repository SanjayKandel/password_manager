# password_manager
Password management tool

files:
1. setting.py - Database creation and for the creation of master key for accessing and updating the password database
2. pass_generator.py -  File for the generation of new passwords and retrieving old generated password
3. main.db - Database file which stores the data i.e passwords username and website. It will be created when you run settings.py and say yes.
4. apps/gui.py: GUI version of this password manager

Steps to use password manager:
1. First of all install all the required libraries from requirements.txt file
2. Then run setting.py file to create the database and setup your master password for accessing database
3. Now you can run the apps/client.py file to manage passwords from terminal or apps/gui.py to manage passwords in a Graphical user interface
