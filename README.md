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

The data came from a spreadsheet I found online.  The files are in the /datasets folder.  You can check them out yourself.  There is the main file {2020_USRC_Group_Detail.xlsx} and then the .csv exports I made from that file.  The export files have been massaged to get into MongoDB properly.  I had to run regex on the original files and then modify to remove [mixed fields] and stuff.  All in all, it was fun and helped to break some of that rust out the old database fingers.

I probably should've used PostGresSqL, but I didn't know the data well enough when I started the project so I went with MongoDB because I already had an account. Now, I see the relational data and some of the lookup tables I can make in PostGresSql when I migrate the app over to relational data and Django Models.  It wasn't that difficult to get the app working without models.  The hardest part was finding the right information in Google.  Phase Two or Three will be relational data; and the models are in the model folder...but they're useless now.  Maybe a base foundation for the PostGresSQL models???

## Debugging
I managed to get the launch.json working on my laptop for the debugger.  It should be in the .vsCode folder.  Hopefully it works for you.  I used the Python Debugger: Django (forms).




