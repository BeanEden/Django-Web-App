from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
from django.urls import path

from authentication.views import SignUpView, upload_profile_photo
import review.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
        name='login'),
    path('logout/', LogoutView.as_view(),
         name='logout'),
    path('signup/', SignUpView.as_view(),
         name='signup'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
        name='password_change'),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
        name='password_change_done'),


    path('profile-photo/upload', upload_profile_photo,
         name='upload_profile_photo'),


    path('home/', review.views.GlobalFeed.as_view(
        template_name = 'home.html'
    ), name='home'),
    path('follow_users/', review.views.follow_users, name='follow_users'),
    path('followed_feed/', review.views.FollowedFeed.as_view(
        template_name='followed_feed.html'
    ), name='followed_feed'),
    path('user_feed/', review.views.GlobalFeed.as_view(
         template_name = 'user_feed.html'), name='user_feed'),
    path('users_followed_feed/', review.views.users_followed_feed, name='users_followed_feed'),
    # path('user_delete/<int:user_follows_id>/', review.views.user_delete, name='user_delete'),

    path('ticket/create/', review.views.TicketCreateView.as_view(
        template_name = 'ticket/ticket_create.html'),
         name='ticket_create'),
    path('ticket/<int:ticket_id>/edit/', review.views.TicketViewAndEdit.as_view(
        template_name='ticket/ticket_edit.html'),
         name='ticket_edit'),
    path('ticket/<int:ticket_id>/delete/', review.views.DeleteView.as_view(
        template_name = 'ticket/ticket_delete.html'),
         name='ticket_delete'),
    path('ticket/<int:ticket_id>/', review.views.TicketViewAndEdit.as_view(
        template_name = 'ticket/ticket_view.html'),
        name='ticket_view'),
    path('ticket_feed/', review.views.GlobalFeed.as_view(
             template_name = 'ticket/ticket_feed.html'), name='ticket_feed'),
    path('ticket_unchecked_feed/', review.views.GlobalFeed.as_view(
             template_name = 'ticket/ticket_unchecked_feed.html'), name='ticket_unchecked_feed'),
#
    path('review/create_with_ticket/', review.views.ReviewCreate.as_view(
        template_name = 'review/review_and_ticket_creation.html'), name='review_and_ticket_creation'),
    path('review/on_<int:ticket_id>/', review.views.ReviewCreate.as_view(
        template_name = 'review/review_on_existing_ticket.html'), name='review_on_existing_ticket'),
    path('review/<int:review_id>/edit', review.views.ReviewViewAndEdit.as_view(
            template_name = 'review/review_edit.html'),
            name='review_edit'),
    path('review/<int:review_id>', review.views.ReviewViewAndEdit.as_view(
                template_name = 'review/review_view.html'),
                name='review_view'),
  path('review/<int:review_id>/delete/', review.views.DeleteView.as_view(
            template_name = 'review/review_delete.html'),
             name='review_delete'),
    path('review_feed/', review.views.GlobalFeed.as_view(
             template_name = 'review/review_feed.html'), name='review_feed'),
#
#     path('profile/', review.views.ProfileTemplateView.as_view(template_name='profile.html'), name='profile'),

    path('ticket_list/', review.views.TicketListView.as_view(template_name = 'ticket_list.html'))

    ]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
