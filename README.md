# For example purposes only.

If you know python, it seems logical on how to run it.
*If you don't then you need to do a few things to get it to run.

### Don't know Django?
1. You will need Django installed
2. Try this if you're a newb: [Geeks for geeks tutorial](https://www.geeksforgeeks.org/python/how-to-create-a-basic-project-using-mvt-in-django/)

## Setup Instructions
**(install django in step 3, after setting up venv)**
1. download and open base folder in VSCode
2. *type in terminal window:*  venv\Scripts\activate
3. *type in terminal window:*  pip install django
4. *cd djangoform*

Production:
5. *type in terminal window:* py manage.py collectstatic

Development:
5. skip this step and try a hard refresh in your browser to see if the files show up.  If not, then
   run collectstatic

6. *type in terminal window:*  py manage.py runserver
7. http://127.0.0.1/



# A little background information
This app is the result of a software engineering spirit and passsion inside of me.  Python has been around for over a decade now and I thought I should take the time to learn it. This is proof, to myself, that I can do it...and I still love software development!

The data came from a spreadsheet I found online.  The files are in the /datasets folder.  On the master branch you'll find the mongoDB version of the app with all of the original files (check the readme there).  In this postGres branch of the app, I used Aiven to setup an account and a database.  Then I used PGAdmin to populate the data into the tables.  My first run at the postGres side of things was with supabase, but I couldn't figure out how to get it to connect.  I tried everything.  Anyhow, the interface was better so I used the SQL Query tool to massage the data into the appropriate places as I normalized it. 

## PostGresSQL data
You will find the .sql files to build the tables and the table row data in .csv files.  Check out the /datasets folder and you can build the db for yourself and use this app to connect to it!  

## MySql data
**I Had problems connecting to Aiven and Supabase without a paid account for PostGresSql hosting.  So...I went ahead and used pythonanywhere's built-in MySql database.**
- I added a mysql_models.py file in the /models folder.
- I added a mysql_schema.sql file in /datasets/db_schemas folder.
- *I did not update the settings.py file to reflect the changes I made for pythonanywhere.com hosting.  If you want help, dm me or something here on github.

**To get this working on _pythonanywhere_ took about 10 hours or so.  _If you need help_, here some things I had to change on the platform:**
 - settings.py
    - DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
    - ALLOWED_HOSTS = ['garuwun.pythonanywhere.com', 'www.garuwun.pythonanywhere.com', '127.0.0.1', 'localhost']
    - DATABASES = {  
          'default': {  
              'ENGINE': 'django.db.backends.mysql',  
              'NAME': '<your_username>$<database_name>',  
              'USER': '<your_username>',  
              'PASSWORD': '<your_mysql_password>',  
              'HOST': '<mysql_hostname>',  
              'PORT': '3306',  
          }  
      }
- in my virtual environment console, I ran 'pip install mysqlclient' because it was originally supposed to be postGresSql
- also, don't forget to run 'py manage.py collectstatic' to get the css and javascript!



## PythonAnywhere
This is hosted on PythonAnywhere here: [USRC 2020 Data Query](https://garuwun.pythonanywhere.com/)


## Debugging
I managed to get the launch.json working on my laptop for the debugger.  It should be in the .vsCode folder.  Hopefully it works for you.  I used the Python Debugger: Django (forms).



