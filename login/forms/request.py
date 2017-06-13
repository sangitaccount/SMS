from django import forms

class RequestForm(forms.Form):
   mobileno = forms.CharField(required=True)
   message = forms.CharField(required=True)
