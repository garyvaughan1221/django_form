from djangoform.mongo_conn import get_client, get_db, close_client
import sys, atexit
from django import forms


## GLOBAL VARS
theDB = None

# I could've just used a function instead of a class, but this is for example purposes
class DbClient():
    """
    Class to get MongoDB database from 2020USRC

    usage: myMongoDB = DBClient.getDB()
    """


    # reset dbConn to None before any actions
    def __init__(self):
        global theDB
        theDB = get_db()
        atexit.register(self.cleanup)

    def cleanup(self):
        print("closing DB connection")
        close_client()


    @classmethod
    def getDB(cls):
        """
        A class method to get the dbConnection
        """

        try:
            client = get_client()
            print("Connected to MongoDB server:", client.address)

            # If MONGODB_DB is set, show collections in that DB. Else list DB names.
            db_name = "2020USRC"
            if db_name: #could be a param...
                theDB = get_db()
                print(f"Using DB: {db_name}")
                print("Collections:", theDB.list_collection_names())

            return theDB

        except Exception as e:
            print("Error connecting to MongoDB:", e, file=sys.stderr)
            sys.exit(2)



class ChurchSearchForm(forms.Form):
    """Returns the form vars and controls

    Use in views.py or a views python/django file
    """

    searchQuery = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}) )

    ddlOptions = (
        ('national', 'National'),
        ('by_state', 'By State'),
        ('by_metro', 'By Metro'),
        ('by_county', 'By County')
    )
    searchType = forms.ChoiceField(choices=ddlOptions,
                                   label="Choose an option",
                                   widget=forms.Select(attrs={'class': 'form-select'}))


def GetChurchesSummary():
    """
    Get the Summary/Totals of Church Organizations in the US during year 2020

    returns: None or a dbCollection, so check for None in calling code
    """
    global theDB
    dbCollection = None

    try:
        theDB = DbClient.getDB()

        if(theDB is not None):
            dbCollection = theDB.summary
            print("there is a collection")

    except Exception as e:
        print (f"Error connecting to MongoDB Collection: {dbCollection}", e, file=sys.stderr)

    finally:
        return dbCollection
