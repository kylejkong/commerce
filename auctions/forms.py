from typing import Text
from django import forms

from django.forms import ModelForm, Textarea, Select, TextInput, \
    NumberInput, PasswordInput

from .models import *


category_choices = Category.objects.all().values_list('category', 'category')
choice_list = []
for item in category_choices:
    choice_list.append(item)

class Create_form(ModelForm):
    class Meta:
        model = Listing
        fields = ["item_name", "item_description", "category", "bids", "img_url"]
        widgets ={
            "item_name": TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Please Enter Item Name(Required!)'
            }),
            'category' : forms.Select(choices=Category.objects.all(), attrs={'class' : 'form-control'}),
            
            "item_description": Textarea(attrs={
                'class': 'form-control', 'placeholder': 'Describle What You Are Seling(Required!)'
            }),
            "img_url": TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Paste Image URL (Optional)'
            }),
            "bids":NumberInput(attrs={
                'class':'form-control', 'min':'1', 'placehoder': 'Enter Starting Bid(Required!)'
            })
            # minimum number is set to 1 and  step : 0.05 meaning the jump is 0.05 at a time.
        }






class Bid_form(ModelForm):
    class Meta:
        model = Bid
        fields = ['price']
        
class Comment_form(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets ={
            "comment": TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Tell Us What You Think'
            })}

