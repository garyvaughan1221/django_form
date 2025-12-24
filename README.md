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
7. There ain't no home page for base path, so navigate to this url: http://127.0.0.1:8000/form/
    ...or http://127.0.0.1/churches/



# A little background information
This app is the result of a software engineering spirit and passsion inside of me.  Python has been around for over a decade now and I thought I should take the time to learn it. This is proof, to myself, that I can do it...and I still love software development!

The data came from a spreadsheet I found online.  The files are in the /datasets folder.  On the master branch you'll find the mongoDB version of the app with all of the original files (check the readme there).  In this postGres branch of the app, I used Aiven to setup an account and a database.  Then I used PGAdmin to populate the data into the tables.  My first run at the postGres side of things was with supabase, but I couldn't figure out how to get it to connect.  I tried everything.  Anyhow, the interface was better so I used the SQL Query tool to massage the data into the appropriate places as I normalized it.

## Debugging
I managed to get the launch.json working on my laptop for the debugger.  It should be in the .vsCode folder.  Hopefully it works for you.  I used the Python Debugger: Django (forms).

## PostGresSQL data
You will find the .sql files to build the tables and the table row data in .csv files.  Check out the /datasets folder and you can build the db for yourself and use this app to connect to it!  

## PythonAnywhere
I'll eventually host the app on pythonAnywhere (first) and then somewhere else possibly, as I feel I will have a need for this data in the next five years before the next census occurs.




