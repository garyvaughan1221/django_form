from datetime import date
from django.shortcuts import render, redirect
from .forms import form1 as f
from .forms import churches as c
from .forms import state_names as sn
from .forms import metro_names as mn
import sys



def form1_view(request):
    """View used for html/input_form.html template

    Handles POST and GET methods
    """

    if request.method == "POST":
        form = f.InputForm(request.POST)

        if form.is_valid():
            # Process the form data
            acceptedNames = ["BlackIce", "SweetTea", "Pythonista", "CodeMaster"]
            name = form.cleaned_data.get("handle")
            if name not in acceptedNames:
                form.add_error("handle", "This handle is invalid. Try again poser!")

            acceptedPasscodes = ["alpha1", "bravo2", "charlie3", "delta4"]
            passcode = form.cleaned_data.get("passcode")
            if passcode not in acceptedPasscodes:
                # Passcode is not accepted
                form.add_error("passcode", "This passcode is invalid. Try again or prepare for consequences...")

            regDate = form.cleaned_data.get("date")
            if regDate is not None:
                if regDate < date(2012, 12, 21):
                    form.add_error("date", "You are not of the Warrior sect.")

            if form.errors:
                return render(request, "input_form.html", {"form": form})
            else:
                return render(request, "submitted.html", {"form": form})
    else:
        # Initial GET request
        form = f.InputForm()
    return render(request, "input_form.html", {"form1": form})


def churches_view(request):
    """View used for html/churches.html template

    Handles POST and GET methods
    """

    # this is for debugging
    printOut = "None"
    PER_PAGE = 5

    if request.method == "POST":
        form = c.ChurchSearchForm(request.POST)

        # ---->  hopefully doesn't bug this <---------------
        request.session["post_flag"] = False

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


            ## TODO: REFACTOR THIS CODE.  may need to move up above
            selectedCounty = form.cleaned_data["countyNames"]
            if(searchType == 'by_county'):
                request.session["selectedCounty"] = selectedCounty
                request.session["selectedState"] = form.cleaned_data["stateNames"]
            else:
                if("selectedCounty" in request.session):
                    del request.session["selectedCounty"]
                    form.cleaned_data["countyNames"] = "0"


            # check & del or set 'metroName' session var
            if(searchType != 'by_metro'):
                if("selectedMetro" in request.session):
                    del request.session["selectedMetro"]
                    form.cleaned_data["metroNames"] = "0"
            else:
                request.session["selectedMetro"] = form.cleaned_data["metroNames"]



            return redirect("/churches")


        # return back to initial form, form was not valid()
        return render(request, 'churches.html', {'form': form})

    ## GET REQUESTS --->
    else:
        context = {}
        searchQuery = ""

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
                selectedMetro = subSearchQuery
                selectedCounty = "0"
                stateName = ""


                # checking selectedState stuff, if conditions met, it's a STATE search....or COUNTY search
                if("selectedState" in request.session):
                    selectedState = request.session["selectedState"]
                    if(selectedState != '0'):
                        subSearchQuery = selectedState
                        stateName = sn.getStateNamebyCode(selectedState)

                    if("selectedCounty" in request.session):
                        selectedCounty = request.session["selectedCounty"]

                # checking selectedMetro stuff, if conditions met, it's a METRO search
                if("selectedMetro" in request.session):
                    selectedMetro = request.session["selectedMetro"]
                    if(selectedMetro != '0'):
                        subSearchQuery = selectedMetro


                form = c.ChurchSearchForm(initial=form_data)
                context = { "form":form, "printOut":printOut }

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
                        context["stateName"] = stateName

                    case 'by_metro':
                        context["metroData"] = searchResults
                        context["selectedMetro"] = selectedMetro

                    case 'by_county':
                        print("by_county")
                        context["selectedCounty"] = selectedCounty
                        context["selectedState"] = selectedState
                        context["stateName"] = stateName
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
                        context["stateName"] = sn.getStateNamebyCode(subSearchQuery)

                    if('selectedMetro' in request.session):
                        subSearchQuery = request.session["selectedMetro"]
                        context["selectedMetro"] = subSearchQuery

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
                        case 'by_metro':
                            context["metroData"] = searchResults
                        case 'by_county':
                            context["countyData"] = searchResults

                else:
                    form = c.ChurchSearchForm()
                    summaryData = getSummaryData()
                    if not summaryData:
                        #reset from list to None for frontEnd
                        summaryData = None

                    context["summaryData"] = summaryData

                context["form"] = form

        except Exception as e:
            print (f"\r\n\t!!!Error in views.churches_view > GET requests:", e, file=sys.stderr)

        finally:
            return render(request, "churches.html", context)





def getSummaryData():
    try:
        #setup initial summary data query
        listData = []
        summary = c.GetChurchesSummary()
        if(summary is not None):
            listData = summary.find({})
            listData = listData[0]

    except Exception as e:
        print (f"Error in views.churches_view: {e}", e, file=sys.stderr)

    finally:
        return listData



def getSearchRegionData(searchType, searchQuery, page_number, per_page, optionalSubQuery:str="0", optionalSelectedCounty:str="0"):
    """
    A helper function to get paged data by search region

        *shouldn't be any other values, it comes from a form...
    """
    match searchType:
        case 'national':
            print('\r\n is national query\r\n')
            result = c.GetNationalData(searchQuery)

        case 'by_state':
            print("\tviews.getSearchRegionData: by_state", optionalSubQuery)
            result = c.GetData_byState(searchQuery, optionalSubQuery)

        case 'by_metro':
            print("\tby metro!", optionalSubQuery)
            result = c.GetData_byMetro(searchQuery, optionalSubQuery)

        case 'by_county':
            print(f"\tVIEWS.PY >> by county...[state] {optionalSubQuery}\t[county]: {optionalSelectedCounty}")

            optionalSubQuery = sn.getStateNamebyCode(optionalSubQuery)
            result = c.GetData_byCounty(searchQuery, optionalSubQuery, optionalSelectedCounty)

    # will return [] or some data...
    return c.getPagedData(result, page_number, per_page)