from django import forms

class AddForm(forms.Form):
    addItem = forms.CharField(widget=forms.HiddenInput())