from datetime import date
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import form1 as f
from .forms import churches as c
from .forms import state_names as sn
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
            request.session["searchQuery"] = form.cleaned_data["searchQuery"]
            request.session["searchType"] = form.cleaned_data["searchType"]
            request.session["selectedState"] = form.cleaned_data["stateNames"]
            return redirect("/churches")

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
                # if(request.session["form_data"]):
                form_data = request.session["form_data"]
                searchType = request.session["searchType"]
                searchQuery = request.session["searchQuery"]
                subSearchQuery = "0"

                selectedState = request.session["selectedState"]
                if(selectedState != '0'):
                    subSearchQuery = selectedState

                form = c.ChurchSearchForm(initial=form_data)
                context = { "form":form, "printOut":printOut }

                # add them back to the context for the form
                context["searchType"] = searchType
                context["query"] = searchQuery
                searchResults = getSearchRegionData(searchType, searchQuery, page_number, PER_PAGE, subSearchQuery)

                match searchType:
                    case 'national':
                        context["nationalData"] = searchResults
                    case 'by_state':
                        context["stateData"] = searchResults
                        context["selectedState"] = selectedState
                        context["stateName"] = sn.getStateNamebyCode(subSearchQuery)[1]

                        # context["printOut"] = sn.getStateNamebyCode(selectedState)[1]



            ## handles 'initial page load' and pagination requests
            else:
                if(page_number):# this is a paging request
                    form_data = request.session["form_data"]
                    form = c.ChurchSearchForm(initial=form_data)
                    subSearchQuery = ""

                    if(request.session["searchType"]):
                        searchType = request.session["searchType"]
                        context["searchType"] = searchType

                    if(request.session["searchQuery"]):
                        searchQuery = request.session["searchQuery"]
                        context["query"] = searchQuery

                    if(request.session["selectedState"]):
                        subSearchQuery = request.session["selectedState"]
                        context["selectedState"] = subSearchQuery
                        context["stateName"] = sn.getStateNamebyCode(subSearchQuery)[1]
                        # context["printOut"] = f"statname: {StateName}"
                        # print(f"out: --> {sn.getStateNamebyCode(subSearchQuery)}")


                    # now get the data
                    searchResults = getSearchRegionData(searchType, searchQuery, page_number, PER_PAGE, subSearchQuery)

                    match searchType:
                        case 'national':
                            context["nationalData"] = searchResults
                        case 'by_state':
                            context["stateData"] = searchResults

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
            print (f"\r\n\t!!!Error in views.churches_view:", e, file=sys.stderr)

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
            if(result is not None):
               return c.getPagedData(result, page_number, per_page)

        case 'by_state':
            print("\tviews.getSearchRegionData: by_state", optionalSubQuery)
            result = c.GetData_byState(searchQuery, optionalSubQuery)
            if(result is not None):
                return c.getPagedData(result, page_number, per_page)

        case 'by_metro':
            print("\tby metro!")
            return None

        case 'by_county':
            print("\tby county...")
            return None