from django.shortcuts import render, redirect
from .forms import churches as c
import sys
from typing import Any, Dict



def churches_view(request):
    """View used for html/churches.html template

    Handles POST and GET methods
    """

    PER_PAGE = 5

    if request.method == "POST":
        form = c.ChurchSearchForm(request.POST)
        request.session["post_flag"] = False

        if("countyChoices" in request.session):
            form.fields["countyNames"].choices = request.session["countyChoices"]

        if form.is_valid():
            request.session["post_flag"] = True
            request.session["form_data"] = form.cleaned_data
            request.session["searchType"] = form.cleaned_data["searchType"]
            request.session["searchQuery"] = form.cleaned_data["searchQuery"]

            print(f"searchType?:", request.session["searchType"])


            ## Need to clear this out for switching between searchTypes...for the dropdown to reset

            # check & del or set 'selectedState' session var
            searchType = request.session["searchType"]
            if(searchType != 'by_state' and searchType != 'by_county'):
                if("selectedState" in request.session):
                    print("deleting selectedState session var")
                    del request.session["selectedState"]
                    form.cleaned_data["stateNames"] = '0'
            else:
                request.session["selectedState"] = form.cleaned_data["stateNames"]

            # check & del or set 'selectedCounty' session var
            selectedCounty = form.cleaned_data["countyNames"]
            if(searchType == 'by_county'):
                request.session["selectedCounty"] = selectedCounty
                request.session["selectedState"] = form.cleaned_data["stateNames"]
            else:
                if("selectedCounty" in request.session):
                    del request.session["selectedCounty"]
                    form.cleaned_data["countyNames"] = "0"


            return redirect("/")
        else:
            print(f"\t--->\tForm is NOT valid\t<---\t")

        # return back to initial form, form was not valid()
        return render(request, 'churches.html', {'form': form})

    ## GET REQUESTS --->
    else:
        searchQuery = ""
        context: Dict[str, Any] = {}

        try:
            page_number = request.GET.get('page')
            post_flag = request.session.get("post_flag")

            if(post_flag):
                #resets the form with the reset-link
                del request.session["post_flag"]
                print("\r\n----> POST FLAG\r\n")

                # technically the app should never post without form_data...
                if('form_data' not in request.session):
                    raise Exception ("No form data!!!")

                form_data = request.session["form_data"]
                searchType = request.session["searchType"]
                searchQuery = request.session["searchQuery"]
                subSearchQuery = "0"
                selectedState = subSearchQuery
                selectedCounty = "0"
                stateName = ""

                form = c.ChurchSearchForm(initial=form_data)
                context = { "form":form }


                # checking selectedState stuff, if conditions met, it's a STATE search....or COUNTY search
                if("selectedState" in request.session):
                    selectedState = request.session["selectedState"]
                    if(selectedState != '0'):
                        subSearchQuery = selectedState

                        if(searchType == 'by_county'):
                            countyChoices = c.GetCountiesForState(selectedState)
                            form.fields["countyNames"].choices = countyChoices
                            request.session["countyChoices"] = countyChoices

                    if("selectedCounty" in request.session):
                        selectedCounty = request.session["selectedCounty"]

                # add these vars back to the context for the form
                context["query"] = searchQuery
                context["searchType"] = searchType

                searchResults = getSearchRegionData(searchType, searchQuery, page_number, PER_PAGE, subSearchQuery, selectedCounty)

                match searchType:
                    case 'national':
                        context["nationalData"] = searchResults

                    case 'by_state':
                        context["stateData"] = searchResults
                        context["selectedState"] = selectedState

                    case 'by_county':
                        print("by_county")
                        context["selectedCounty"] = selectedCounty
                        context["selectedState"] = selectedState
                        context["countyData"] = searchResults

                print("------------>  END postFlag <-------------------")


            ## handles 'initial page load' and pagination requests
            else:
                if(page_number):# this is a paging request
                    form_data = request.session["form_data"]
                    form = c.ChurchSearchForm(initial=form_data)
                    subSearchQuery = ""

                    if('searchType' in request.session):
                        searchType = request.session["searchType"]
                        context["searchType"] = searchType

                    if('searchQuery' in request.session):
                        searchQuery = request.session["searchQuery"]
                        context["query"] = searchQuery

                    if('selectedState' in request.session):
                        subSearchQuery = request.session["selectedState"]
                        context["selectedState"] = subSearchQuery

                        if(searchType == "by_county"):
                            countyChoices = c.GetCountiesForState(subSearchQuery)
                            form.fields["countyNames"].choices = countyChoices
                            request.session["countyChoices"] = countyChoices

                    if('selectedCounty' in request.session):
                        selectedCounty = request.session["selectedCounty"]
                        context["selectedCounty"] = selectedCounty
                    else:
                        selectedCounty = "0"

                    # now get the data
                    searchResults = getSearchRegionData(searchType, searchQuery, page_number, PER_PAGE, subSearchQuery, selectedCounty)

                    match searchType:
                        case 'national':
                            context["nationalData"] = searchResults
                        case 'by_state':
                            context["stateData"] = searchResults
                        case 'by_county':
                            context["countyData"] = searchResults

                # initial page load
                else:
                    form = c.ChurchSearchForm()
                    summaryData = c.GetChurchesSummary()
                    if not summaryData:
                        #reset from list to None for frontEnd
                        summaryData = None

                    context["summaryData"] = summaryData

                context["form"] = form

        except Exception as e:
            print (f"\r\n\t!!!Error in views.churches_view > GET requests:", e, file=sys.stderr)

        finally:
            return render(request, "churches.html", context)



def getSearchRegionData(searchType, searchQuery, page_number, per_page, optionalSubQuery:str="0", optionalSelectedCounty:str="0"):
    """
    A helper function to get paged data by search region

        *shouldn't be any other values, it comes from a form...

    returns: [] or list Data
    """
    match searchType:
        case 'national':
            print('\r\n is national query\r\n')
            result = c.GetNationalData(searchQuery)

        case 'by_state':
            print("\tviews.getSearchRegionData: by_state", optionalSubQuery)
            result = c.GetData_byState(searchQuery, optionalSubQuery)

        case 'by_county':
            print(f"\tVIEWS.PY >> by county...[state] {optionalSubQuery}\t[county]: {optionalSelectedCounty}")

            result = c.GetData_byCounty(searchQuery, optionalSubQuery, optionalSelectedCounty)

    # will return [] or some data...
    return c.getPagedData(result, page_number, per_page)