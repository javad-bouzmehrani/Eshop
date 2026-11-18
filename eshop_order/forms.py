from django import forms

class User_neworder_Form(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    count = forms.IntegerField(
        initial=1,
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={
            'class': 'qty-input',
            'id': 'quantity-display',
        }),
    )