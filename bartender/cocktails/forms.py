from django import forms

class search_cocktail(forms.Form):
    search = forms.CharField(label='Search',max_length=300)
