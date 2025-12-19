import sys
from django import forms
from django.db.models import Subquery, OuterRef
from djangoform.api.db_client import DbClient
from djangoform.models.postgres_models import National as National_dbQuery, ChurchOrgs
from djangoform.api.by_state import State_dbQuery
from djangoform.api.by_county import County_dbQuery
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
        ('by_county', 'By County')
    )
    searchType = forms.ChoiceField(choices=ddlOptions,
                                   label="Choose an option",
                                   widget=forms.Select(attrs={'class': 'form-select'}))

    # statename_choices = sn.stateNames
    # stateNames = forms.ChoiceField(choices=statename_choices,
    #                                 label="select a state",
    #                                 widget=forms.Select(attrs={'class': 'form-select'}))

    countyNames = forms.ChoiceField(
        choices= [( "0", "select a county")],
        label="Select a County",
        widget=forms.Select(attrs={'class': 'form-select'}))


##
def GetChurchesSummary():
    """
        Function to get the Churches Summary data

        *hardcoded JSON.
    """

    try:
        listData = {
            "Congregations": 356642,
            "Adherents": 161224088,
            "Adherents_percent_of_Population": 48.64,
            "Population_2020": 331449281,
            "Congregations_per_1000_population": 107.6
        }

    except Exception as e:
        print (f"Error in churches.GetChurchesSummary()", e, file=sys.stderr)

    finally:
        return listData



## TODO: byChurchOrg <click_event>
def GetNationalData(searchQuery:str):
    """
    Function to get the National Data by various search queries

    { byChurchOrg, likeTxtSearch }
    - returns empty list, or a dbCollection
    """

    try:
        listData = []

        # Subquery to get GroupName from ChurchOrgs using GroupCode
        orgs_qs = ChurchOrgs.objects.filter(groupcode=OuterRef('groupcode')).values('groupname')[:1]

        qs = National_dbQuery.objects.annotate(groupname=Subquery(orgs_qs))

        if searchQuery and searchQuery != "all":
            qs = qs.filter(groupname__icontains=searchQuery)

        listData = list(qs.values())

    except Exception as e:
        print (f"Error in churches.GetNationalData()", e, file=sys.stderr)

    finally:
        return listData


##
def GetData_byState(searchQuery:str, subSearchQuery:str='0'):
    """
    Function to get the data by State with search query

    {subSearchQuery} param is the selected U.S. State

    - returns empty list, or a dbCollection
    """

    try:
        listData = []
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


def GetData_byCounty(searchQuery:str, selectedState:str='0', selectedCounty:str="0"):
    """
    Function to get the data by State & County with search query

    - returns empty list, or a dbCollection
    """

    try:
        listData = []
        theDB = DbClient.getDB()
        if(theDB is not None):
            dbCollection = theDB.by_county

            print(f"GetData_byCounty({searchQuery}, {selectedState}, {selectedCounty})")

            if(selectedState == ''):
                raise Exception (f"churches.GetData_byCounty({searchQuery}, {selectedState}, {selectedCounty}) -->>\t selectedState is blank for some reason")

            ## get data
            listData = County_dbQuery.getData(dbCollection, searchQuery, selectedState, selectedCounty)

    except Exception as e:
        print (f"Error in churches.GetData_byCounty({searchQuery}, {selectedState}, {selectedCounty})", e, file=sys.stderr)

    finally:
        return listData


def GetCountyNames(searchQuery:str, selectedState:str):
    """
    Function to get County Names per selectedState

    {param: type} searchQuery: str
    {param: type} selectedState: str
    """
    selectedCounty = "0"
    countyNames = []

    try:
        theDB = DbClient.getDB()
        if(theDB is not None):
            dbCollection = theDB.by_county
            countyNames = County_dbQuery.getCountyNamesListForSelectedState(dbCollection, searchQuery, selectedState)

    except Exception as e:
        print(f"Error with MongoDB queries in chuches.getCountyNames({searchQuery}, {selectedState})", e, file=sys.stderr)
        sys.exit(2)
    finally:
        return countyNames



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