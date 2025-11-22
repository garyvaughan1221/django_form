from datetime import date
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import form1 as f
from .forms import churches as c
import sys
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



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

            # TODO having issues with pulling these out of form_data in -GET- clause
            request.session["searchType"] = form.cleaned_data["searchType"]
            request.session["searchQuery"] = form.cleaned_data["searchQuery"]
            return redirect("/churches")


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
                selectedSearchRegion = request.session["searchType"]
                searchQuery = request.session["searchQuery"]

                form = c.ChurchSearchForm(initial=form_data)
                context = { "form":form, "printOut":printOut }

                # add them back to the context for the form
                context["selected_id"] = selectedSearchRegion
                context["query"] = searchQuery
                searchResults = getSearchRegionData(selectedSearchRegion, searchQuery, page_number, PER_PAGE)

                match selectedSearchRegion:
                    case 'national':
                        context["nationalData"] = searchResults
                    case 'by_state':
                        context["stateData"] = searchResults


            ## handles 'initial page load' and pagination requests
            else:
                if(page_number):# this is a paging request
                    form_data = request.session["form_data"]
                    form = c.ChurchSearchForm(initial=form_data)

                    # TODO: need to branch logic for searchType again...
                    # these should be there if page_number...however
                    if(request.session["searchType"]):
                        selectedSearchRegion = request.session["searchType"]
                        context["selected_id"] = selectedSearchRegion

                    if(request.session["searchQuery"]):
                        searchQuery = request.session["searchQuery"]
                        context["query"] = searchQuery

                    # now get the data
                    searchResults = getSearchRegionData(selectedSearchRegion, searchQuery, page_number, PER_PAGE)

                    match selectedSearchRegion:
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
            print (f"\r\n\t!!!Error:", e, file=sys.stderr)

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



def getSearchRegionData(selectedSearchRegion, searchQuery, page_number, per_page):
    """
    A helper function to get paged data by search region

        *shouldn't be any other values, it comes from a form...
    """
    match selectedSearchRegion:
        case 'national':
            print('\r\n is national query\r\n')
            result = c.GetNationalData(searchQuery)
            if(result is not None):
               return c.getPagedData(result, page_number, per_page)

        case 'by_state':
            print("\tby state")
            result = c.GetData_byState(searchQuery)
            if(result is not None):
                return c.getPagedData(result, page_number, per_page)

        case 'by_metro':
            print("\tby metro!")
            return None

        case 'by_county':
            print("\tby county...")
            return None