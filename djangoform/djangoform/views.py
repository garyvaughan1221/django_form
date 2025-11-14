from datetime import date
from django.http import HttpResponse
from django.shortcuts import render
from .forms import form1 as f
from .forms import churches as c


def form1_view(request):
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
    if request.method == "POST":
        form = c.ChurchSearch(request.POST)

        if form.is_valid():
            # Process the form data
            searchQuery = form.cleaned_data.get("searchQuery")

    else:
        form = c.ChurchSearch()
        return render(request, "churches.html", {"form": form})