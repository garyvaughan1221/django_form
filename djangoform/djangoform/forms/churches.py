import sys
from django.db.models import Subquery, OuterRef
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# custom code stuff
from django import forms

# models
from djangoform.models.mysql_models import National as National_dbQuery, ChurchOrgs
from djangoform.models.mysql_models import ByState as State_dbQuery
from djangoform.models.mysql_models import ByCounty as County_dbQuery

# for the dropdowns
from djangoform.models.mysql_models import StateNames as StateNames
from djangoform.models.mysql_models import CountyNames as CountyNames



# this is the main class here in this file
class ChurchSearchForm(forms.Form):
    """Returns the form vars and controls

    Use in views.py or a views python/django file
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            # choices for dropdowns
            Statechoices = [('0', 'Select a State')]
            for state in StateNames.objects.all():
                Statechoices.append((state.pk, str(state.statename)))
            self.fields['stateNames'].choices = Statechoices

            CountyChoices = [('0', 'Select a County')]
            for county in CountyNames.objects.all():
                CountyChoices.append((county.pk, str(county.countyname)))
            self.fields['countyNames'].choices = CountyChoices
        except Exception:
            pass

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

    stateNames = forms.ChoiceField(
        choices=[('0', 'Select a State')],
        label="Select a State",
        widget=forms.Select(attrs={'class': 'form-select'}))

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

        # Subquery to get GroupName from ChurchOrgs using GroupCode
        orgs_qs = ChurchOrgs.objects.filter(groupcode=OuterRef('groupcode')).values('groupname')[:1]

        # Subquery to get StateName from StateNames using StateCode
        states_qs = StateNames.objects.filter(pk=OuterRef('statecode')).values('statename')[:1]

        qs = State_dbQuery.objects.annotate(groupname=Subquery(orgs_qs), statename=Subquery(states_qs))

        if searchQuery and searchQuery != "all":
            qs = qs.filter(groupname__icontains=searchQuery)

        if subSearchQuery and subSearchQuery != "0":
            qs = qs.filter(statecode=subSearchQuery)

        listData = list(qs.values())

    except Exception as e:
        print (f"Error in churches.GetData_byState()", e, file=sys.stderr)

    finally:
        return listData



def GetCountiesForState(stateCode):
    """
    Function to get the counties for a selected state

    - returns empty list, or results in a tuple for a dropdown
    """

    try:
        listData = [('0', 'Select a County')]

        for county in CountyNames.objects.filter(statecode=stateCode):
            listData.append((county.pk, str(county.countyname)))

    except Exception as e:
        print (f"Error in churches.GetCountiesForState({stateCode})", e, file=sys.stderr)

    finally:
        return listData


def GetData_byCounty(searchQuery:str, selectedState:str, selectedCounty:str="0"):
    """
    Function to get the data by State & County with search query

    """
    try:
        listData = []

        # Subquery to get GroupName from ChurchOrgs using GroupCode
        orgs_qs = ChurchOrgs.objects.filter(groupcode=OuterRef('groupcode')).values('groupname')[:1]

        # Subquery to get StateName from StateNames using StateCode
        states_qs = StateNames.objects.filter(pk=OuterRef('statecode')).values('statename')[:1]

        # Subquery to get CountyName from CountyNames using CountyCode
        county_qs = CountyNames.objects.filter(pk=OuterRef('fips')).values('countyname')[:1]

        # Main query > sets groupname, statename, countyname instead of {codes}
        qs = County_dbQuery.objects.annotate(groupname=Subquery(orgs_qs), statename=Subquery(states_qs), countyname=Subquery(county_qs))


        # only filter by searchQuery if it's not "all"
        if(searchQuery and searchQuery != "all"):
            qs = qs.filter(groupname__icontains=searchQuery)

        # always filter by state
        qs = qs.filter(statecode=selectedState)

        # only filter by county if a county is selected
        if selectedCounty and selectedCounty != "0":
            qs = qs.filter(fips=selectedCounty)

        listData = list(qs.values())

    except Exception as e:
        print (f"Error in churches.GetData_byCounty({searchQuery}, {selectedState}, {selectedCounty})", e, file=sys.stderr)

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