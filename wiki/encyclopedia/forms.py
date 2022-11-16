import re
from .util import list_entries
from django import forms


class SearchForm(forms.Form):

    keyword = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class NewForm(forms.Form):
    title = forms.CharField(label="Add Title")
    body = forms.CharField(label="Add Body", widget=forms.Textarea(
        attrs={'rows': 5, 'cols': 5}))

class EditPageForm(forms.Form):
    title = forms.CharField(label="Title")
    body = forms.CharField(label="Body", widget=forms.Textarea(
        attrs={'rows': 5, 'cols': 5}))
