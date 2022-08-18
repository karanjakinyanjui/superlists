"""
Author: Elijah Kinyanjui
(c) Copyright by HugosLabs ltd

File: 
Description: 


"""
from django import forms
from django.core.exceptions import ValidationError

from lists.models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"


class ItemForm(forms.ModelForm):

    def save(self, for_list, *args, **kwargs):
        self.instance.list = for_list
        return super().save()

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg',
                'id': "new_item_input",
            })
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }


class ExistingListItemForm(ItemForm):

    def __init__(self, *args, for_list, **kwargs):
        super().__init__(*args, **kwargs)
        self.for_list = for_list
        self.instance.list = for_list

    def save(self, *args, **kwargs):
        return forms.ModelForm.save(self)

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)
