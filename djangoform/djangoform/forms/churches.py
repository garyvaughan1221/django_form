import sys
from django import forms
from djangoform.api.mongo_conn import get_client, get_db, close_client
from djangoform.api.db_client import DbClient
from djangoform.api.national import National_dbQuery
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


## GLOBAL VARS
theDB = DbClient.getDB()



class ChurchSearchForm(forms.Form):
    """Returns the form vars and controls

    Use in views.py or a views python/django file
    """

    searchQuery = forms.CharField(max_length=20, initial="all", widget=forms.TextInput(attrs={'class': 'form-control'}) )

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
            # print("there is a collection")

    except Exception as e:
        print (f"Error connecting to MongoDB Collection: {dbCollection}", e, file=sys.stderr)

    finally:
        return dbCollection


## TODO: branch code for using queries
def GetNationalData(searchQuery:str):
    """
    Function to get the National Data by various search queries

    { byChurchOrg, likeTxtSearch }
    - returns empty list, or a dbCollection
    """
    global theDB
    listData = []

    try:
        theDB = DbClient.getDB()

        if(theDB is not None):
            dbCollection = theDB.national

            #checking for lack of param passed in
            if(searchQuery == "all"):
                listData = National_dbQuery.getAll(dbCollection)
            elif (searchQuery is not None):
                listData = National_dbQuery.querySearch(dbCollection, searchQuery)

    except Exception as e:
        print (f"Error in churches.GetNationalData()", e, file=sys.stderr)

    finally:
        return listData


def getPagedData(data_in:list, page_number:int, per_page:int):
    """
    Function used to get paged data.  Feed in the json object and get a sliced piece of data via Django Paginator class

    returns a list
    """
    paginator = Paginator(data_in, per_page)
    paged_obj = []

    try:
        paged_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        paged_obj = paginator.page(1)
    except EmptyPage:
        paged_obj = paginator.page(paginator.num_pages)
    finally:
        return paged_obj