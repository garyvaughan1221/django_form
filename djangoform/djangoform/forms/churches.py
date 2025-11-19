import sys
from django import forms
from djangoform.api.mongo_conn import get_client, get_db, close_client
from djangoform.api.db_client import DbClient
from djangoform.api.national import National_dbQuery


## GLOBAL VARS
theDB = DbClient.getDB()



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

##
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


##
def GetNationalData():
    """
    Function to get the National Data by various search queries

    { byChurchOrg, likeTxtSearch }
    - returns None, or a dbCollection
    """
    global theDB
    dbCollection = None

    try:
        theDB = DbClient.getDB()

        if(theDB is not None):
            dbCollection = theDB.national
            elQuery = National_dbQuery.getAll(dbCollection)
            return elQuery

    except Exception as e:
        print (f"Error in churches.GetNationalData()", e, file=sys.stderr)
        return dbCollection


