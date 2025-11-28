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
            if(request.session["searchType"] != 'by_state'):
                if("selectedState" in request.session):
                    del request.session["selectedState"]
                    form.cleaned_data["stateNames"] = '0'
            else:
                request.session["selectedState"] = form.cleaned_data["stateNames"]

            # check & del or set 'metroName' session var
            if(request.session["searchType"] != 'by_metro'):
                if('selectedMetro' in request.session):
                    del request.session["selectedMetro"]
                    form.cleaned_data["metroNames"] = '0'
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


                # checking selectedState stuff, if conditions met, it's a STATE search
                if("selectedState" in request.session):
                    selectedState = request.session["selectedState"]
                    if(selectedState != '0'):
                        subSearchQuery = selectedState

                # checking selectedMetro stuff, if conditions met, it's a METRO search
                if("selectedMetro" in request.session):
                    selectedMetro = request.session["selectedMetro"]
                    if(selectedMetro != '0'):
                        subSearchQuery = selectedMetro



                form = c.ChurchSearchForm(initial=form_data)
                context = { "form":form, "printOut":printOut }


                # add these vars back to the context for the form
                searchResults = getSearchRegionData(searchType, searchQuery, page_number, PER_PAGE, subSearchQuery)
                context["query"] = searchQuery
                context["searchType"] = searchType

                match searchType:
                    case 'national':
                        context["nationalData"] = searchResults

                    case 'by_state':
                        context["stateData"] = searchResults
                        context["selectedState"] = selectedState
                        context["stateName"] = sn.getStateNamebyCode(subSearchQuery)

                    case 'by_metro':
                        context["metroData"] = searchResults
                        context["selectedMetro"] = selectedMetro

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


                    # now get the data
                    searchResults = getSearchRegionData(searchType, searchQuery, page_number, PER_PAGE, subSearchQuery)

                    match searchType:
                        case 'national':
                            context["nationalData"] = searchResults
                        case 'by_state':
                            context["stateData"] = searchResults
                        case 'by_metro':
                            context["metroData"] = searchResults

                else:
                    print("NO PAGE_NUMBER?????")

                    form = c.ChurchSearchForm()
                    # print(f"\t\tSUMMARY CLAUSE??: { post_flag }")
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



def getSearchRegionData(searchType, searchQuery, page_number, per_page, optionalSubQuery:str="0"):
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
            print("\tby county...")
            return None

    # will return [] or some data...
    return c.getPagedData(result, page_number, per_page)