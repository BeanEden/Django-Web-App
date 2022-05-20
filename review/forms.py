from django import forms
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()

CHOICES = [('0', 0), ('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)]


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['titre', 'description', 'image']


class ReviewForm(forms.ModelForm):
    edit_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']


class DeleteBlogForm(forms.Form):
    delete_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)


# class UserFollowsForm(forms.ModelForm):
#     edit_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)
#
#     class Meta:
#         model = User
#         fields = ['abonnements']
