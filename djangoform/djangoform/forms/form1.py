from django import forms

class InputForm(forms.Form):
    handle = forms.CharField(max_length=20)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    passcode = forms.CharField(max_length=7, widget=forms.PasswordInput())