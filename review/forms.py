from django import forms
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe


from . import models

User = get_user_model()

CHOICES=[('0',0),('1',1),('2',2),('3',3),('4',4),('5',5)]

# class HorizontalRadioRenderer(forms.RadioSelect):
#    def render(self):
#      return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))
# 
# 
# class ApprovalForm(forms.Form):
#      approval = forms.ChoiceField(
#             choices=CHOICES,
#             initial=0, 
#            widget=forms.RadioSelect(
#                  renderer=HorizontalRadioRenderer
#            ),
#          )


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


class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['follows']


class UserFollowsForm(forms.ModelForm):
    # abonnements = forms.CharField()
    class Meta:
        model = User
        fields = ['abonnements']


# class FollowedUsersForm(forms.ModelForm):
#     class Meta:
#         model = models.FollowedUsers
#         fields = ['user_name']
