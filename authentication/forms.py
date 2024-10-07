from django import forms

class WeightForm(forms.Form):
    weight = forms.FloatField(label='Enter your weight (kg)', min_value=0)
