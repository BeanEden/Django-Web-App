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


    # -------------------------AUTHENTICATION PAGES-------------------------#

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


    # --------------------------HOME AND USER PAGES--------------------------#

    path('home/', review.views.GlobalFeed.as_view(), name='home'),
    path('user_feed/', review.views.UserFeed.as_view(), name='user_feed'),
    path('profile-photo/upload', upload_profile_photo,
         name='upload_profile_photo'),

    # -----------------------------TICKET PAGES-----------------------------#

    path('ticket/create/', review.views.ticket_create, name='ticket_create'),
    path('ticket/<int:ticket_id>/edit/', review.views.ticket_edit,
         name='ticket_edit'),
    path('ticket/<int:ticket_id>/delete/', review.views.ticket_delete,
         name='ticket_delete'),
    path('ticket_feed/', review.views.TicketListView.as_view(
             template_name='ticket/ticket_feed.html'),
         name='ticket_feed'),
    path('ticket_unchecked_feed/', review.views.TicketListView.as_view(
             template_name='ticket/ticket_unchecked_feed.html'),
         name='ticket_unchecked_feed'),
    path('ticket/<int:ticket>/', review.views.ticket_view, name='ticket_view'),


    # -----------------------------REVIEW PAGES-----------------------------#

    path('review/create_with_ticket/', review.views.review_and_ticket_creation,
         name='review_and_ticket_creation'),
    path('review/on_<int:ticket_id>/', review.views.review_on_existing_ticket,
         name='review_on_existing_ticket'),
    path('review/<int:review_id>/edit', review.views.review_edit,
         name='review_edit'),
    path('review/<int:review_id>/delete/', review.views.review_delete,
         name='review_delete'),
    path('review_feed/', review.views.ReviewListView.as_view(),
         name='review_feed'),
    path('review/<int:review_id>/', review.views.review_view,
         name='review_view'),


    # -------------------------FOLLOWED USERS PAGES-------------------------#

    path('follow_users_page/', review.views.follow_users_page,
         name='follow_users_page'),
    path('user_unfollow_page/<int:user_follows_id>/',
         review.views.user_unfollow_page, name='user_unfollow_page'),
    path('followed_feed/', review.views.FollowedFeed.as_view(),
         name='followed_feed'),

    ]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
