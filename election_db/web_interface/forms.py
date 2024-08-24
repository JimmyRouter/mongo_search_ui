from django import forms


class Searches(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    surname = forms.CharField(max_length=100, required=False)
    father_name = forms.CharField(max_length=100, required=False)
    father_surname = forms.CharField(max_length=100, required=False)
    gender = forms.CharField(max_length=1, required=False)
    # dob = forms.DateField(required=False)
    age = forms.IntegerField(required=False)
    address = forms.CharField(required=False)
    party = forms.CharField(max_length=10, required=False)


class Member(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    surname = forms.CharField(max_length=100, required=False)
    father_name = forms.CharField(max_length=100, required=False)
    father_surname = forms.CharField(max_length=100, required=False)
    gender = forms.CharField(max_length=1, required=False)
    dob = forms.DateField(required=False)
    age = forms.IntegerField(required=False)
    address = forms.CharField(required=False)
    party = forms.CharField(max_length=10, required=False)
    _id = forms.CharField(widget=forms.HiddenInput())

