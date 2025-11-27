import sys
from django import forms
from djangoform.api.db_client import DbClient
from djangoform.api.national import National_dbQuery
from djangoform.api.by_state import State_dbQuery
from djangoform.api.by_metro import Metro_dbQuery
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from djangoform.forms import state_names as sn
from djangoform.forms import metro_names as mn


## GLOBAL VARS
theDB = DbClient.getDB()



class ChurchSearchForm(forms.Form):
    """Returns the form vars and controls

    Use in views.py or a views python/django file
    """

    searchQuery = forms.CharField(
        strip=True,
        max_length=20,
        initial="all",
        widget=forms.TextInput(attrs={'class': 'form-control'}) )

    ddlOptions = (
        ('national', 'National'),
        ('by_state', 'By State'),
        ('by_metro', 'By Metro'),
        ('by_county', 'By County')
    )
    searchType = forms.ChoiceField(choices=ddlOptions,
                                   label="Choose an option",
                                   widget=forms.Select(attrs={'class': 'form-select'}))

    statename_choices = sn.stateNames
    stateNames = forms.ChoiceField(choices=statename_choices,
                                    label="Choose a State",
                                    widget=forms.Select(attrs={'class': 'form-select'}))

    metroname_choices = mn.metroNames
    metroNames = forms.ChoiceField(choices= metroname_choices,
                                    label="Choose a Metro",
                                    required=True,
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

    except Exception as e:
        print (f"Error connecting to MongoDB Collection: {dbCollection}", e, file=sys.stderr)

    finally:
        return dbCollection



## TODO: byChurchOrg <click_event>
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


##
def GetData_byState(searchQuery:str, subSearchQuery:str='0'):
    """
    Function to get the date by State with search query

    { byChurchOrg, likeTxtSearch }
    - returns empty list, or a dbCollection
    """
    global theDB
    listData = []

    try:
        theDB = DbClient.getDB()

        if(theDB is not None):
            dbCollection = theDB.by_state

            #checking for lack of param passed in
            print("in here with subsSearchQuery", subSearchQuery)

            # TODO: refactor this 'None' away from here???  INVESTIGATE...
            if(subSearchQuery is None or subSearchQuery == ''):
                raise Exception ("subSearchQuery is none")

            if (searchQuery != "" and int(subSearchQuery) != 0):
                print(f"has state.searchQuery: {searchQuery} and subSearchQuery: {subSearchQuery}")
                listData = State_dbQuery.stateSearch(dbCollection, subSearchQuery, searchQuery)
            elif (searchQuery is not None and searchQuery != "all"):
                print("searchQuery is not None or all", searchQuery)
                listData = State_dbQuery.querySearch(dbCollection, searchQuery)
            elif(searchQuery == "all"):
                print('all by_state')
                listData = State_dbQuery.getAll(dbCollection)


    except Exception as e:
        print (f"Error in churches.GetData_byState()", e, file=sys.stderr)

    finally:
        return listData


def GetData_byMetro(searchQuery:str, subSearchQuery:str='0'):
    """
    Function to get the date by State with search query

    { byChurchOrg, likeTxtSearch }
    - returns empty list, or a dbCollection
    """
    global theDB
    listData = []

    try:
        theDB = DbClient.getDB()

        if(theDB is not None):
            dbCollection = theDB.by_metro

            #checking for lack of param passed in
            print("in here with subsSearchQuery", subSearchQuery)

            # TODO: refactor this 'None' away from here???  INVESTIGATE...
            if(subSearchQuery is None or subSearchQuery == ''):
                raise Exception ("subSearchQuery is none")

            ## has searchQuery and user selected a 'metro area'
            if (searchQuery != "" and int(subSearchQuery) != 0):
                print("has metro subSearchQuery", subSearchQuery)
                print("has metro searchQuery", searchQuery)
                listData = Metro_dbQuery.MetroSearch(dbCollection, subSearchQuery, searchQuery)

            ## user has typed a searchquery in
            elif (searchQuery is not None and searchQuery != "all"):
                print("searchQuery is not None or all", searchQuery)
                listData = Metro_dbQuery.querySearch(dbCollection, searchQuery)

            ## searchQuery is "all", no metro selected
            elif(searchQuery == "all"):
                print('all by_metro')
                listData = Metro_dbQuery.getAll(dbCollection)


    except Exception as e:
        print (f"Error in churches.GetData_byMetro()", e, file=sys.stderr)

    finally:
        return listData







##
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