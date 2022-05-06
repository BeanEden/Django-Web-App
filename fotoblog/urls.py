from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
from django.urls import path

import authentication.views
import review.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(template_name='authentication/login.html', redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', PasswordChangeView.as_view(template_name='authentication/password_change_form.html'),
         name='password_change'),
    path('change-password-done/', PasswordChangeDoneView.as_view(template_name='authentication/password_change_done.html'),
         name='password_change_done'),
    path('signup/', authentication.views.signup_page, name='signup'),


    path('profile-photo/upload', authentication.views.upload_profile_photo,
         name='upload_profile_photo'),


    path('home/', review.views.home, name='home'),
    path('follow_users/', review.views.follow_users, name='follow_users'),
    path('followed_user_feed/', review.views.followed_user_feed, name='followed_user_feed'),
    path('user_feed/', review.views.user_feed, name='user_feed'),


    path('ticket/create/', review.views.ticket_create, name='ticket_create'),
    path('ticket/<int:ticket_id>/edit/', review.views.ticket_edit, name='ticket_edit'),
    path('ticket/<int:ticket_id>/delete/', review.views.ticket_delete, name='ticket_delete'),
    path('ticket/<int:ticket_id>', review.views.ticket_view, name='ticket_view'),
    path('ticket_feed/', review.views.ticket_feed, name='ticket_feed'),
    path('ticket_unchecked_feed/', review.views.ticket_unchecked_feed, name='ticket_unchecked_feed'),

    path('review/create/', review.views.review_create, name='review_create'),
    path('review/create_with_ticket/', review.views.review_and_ticket_creation, name='review_and_ticket_creation'),
    path('review/on_<int:ticket_id>/', review.views.review_on_existing_ticket, name='review_on_existing_ticket'),
    path('review/<int:review_id>/edit', review.views.review_edit, name='review_edit'),
    path('review/<int:review_id>/delete/', review.views.review_delete, name='review_delete'),
    path('review/<int:review_id>', review.views.review_view, name='review_view'),
    path('review_feed/', review.views.review_feed, name='review_feed')

]

# path('follow-users/', review.views.follow_users, name='follow_users')

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
