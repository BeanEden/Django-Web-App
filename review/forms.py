from django import forms
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()

class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['titre', 'description', 'image']


class ReviewForm(forms.ModelForm):
    edit_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']


class DeleteBlogForm(forms.Form):
    delete_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['follows']


class UserFollowsForm(forms.ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ['followed_user']


# class FollowedUsersForm(forms.ModelForm):
#     class Meta:
#         model = models.FollowedUsers
#         fields = ['user_name']
