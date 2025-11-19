from datetime import date
from django.http import HttpResponse
from django.shortcuts import render
from .forms import form1 as f
from .forms import churches as c
from .models import churchModels
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




## CODE LOGIC GOES HERE FOR CHURCHES VIEW
#   1. need to create models
#   2. import db connection
#   3. create logic to query db based on searchQuery form input
#
#  ##

def churches_view(request):
    """View used for html/churches.html template

    Handles POST and GET methods
    """

    if request.method == "POST":
        form = c.ChurchSearchForm(request.POST)

        if form.is_valid():
            # get the search fld value from form
            txtSearchQuery = form.cleaned_data.get("searchQuery")
            selectedSearchReqion = form.cleaned_data.get("searchType")

            ## TODO: need to include logic here to do query from the database

            return render(request, "churches.html", {"form": form, "selected_id": selectedSearchReqion, "query":txtSearchQuery})


    else:
        form = c.ChurchSearchForm()
        elData = None

        try:

            #setup initial summary data query
            myVar = None
            # summary = c.GetChurchesSummary()
            # if(summary is not None):
            #     elData = summary.find({})
            #     elData = elData[0]
            #     print(f"elData {elData}")

        except Exception as e:
            print (f"Error in views.churches_view: {e}", e, file=sys.stderr)

    return render(request, "churches.html", {"form": form, "summaryData": elData})