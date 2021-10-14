# password_manager
Password management tool

files:
1. setting.py - Database creation and for the creation of master key for accessing and updating the password database
2. pass_generator.py -  File for the generation of new passwords and retrieving old generated password
3. main.db - Database file which stores the data i.e passwords username and website. It will be create when you run settings.py and say yes.

Steps to use password manager:
1. First of all install all the required libraries from requirements.txt file
2. Then run setting.py file to create the database and setup you master password for accessing database
3. Now you can run the pass_manager.py file and use it to generate and see saved passwords
