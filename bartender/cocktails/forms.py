from django import forms

class search_drink(forms.Form):
    search = forms.CharField(label='Search',max_length=300)
