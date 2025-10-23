from django.http import HttpResponse
from django.shortcuts import render
from .forms import form1 as f


def form_view(request):
    if request.method == "POST":
        form = f.InputForm(request.POST)
        if form.is_valid():
            # Process the form data
            # return HttpResponse("Form submitted successfully!")
            return render(request, "submitted.html", {"form": form})
    else:
        form = f.InputForm()
    return render(request, "input_form.html", {"form": form})
