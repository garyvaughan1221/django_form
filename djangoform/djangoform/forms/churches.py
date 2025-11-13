from django import forms

class ChurchSearch(forms.Form):
    searchQuery = forms.CharField(max_length=20)