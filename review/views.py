from itertools import chain

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.shortcuts import get_object_or_404, redirect, render

from django.views import View
from django.views.generic.list import ListView

from . import forms, models


User = get_user_model()


# -----------------------------MIXINS-----------------------------#

class PaginatedViewMixin:
    """Mixin to paginate feeds class"""

    @staticmethod
    def paginate_view(request, object_paginated):
        """Method to paginate feed

        arguments: request, post _lit (ex: list of reviews)
        return: post_list paginated"""

        paginator = Paginator(object_paginated, 6)
        page = request.GET.get('page')
        try:
            object_paginated = paginator.page(page)
        except PageNotAnInteger:
            object_paginated = paginator.page(1)
        except EmptyPage:
            object_paginated = paginator.page(paginator.num_pages)
        return object_paginated


# ---------------------------HOME AND USER PAGES---------------------------#

class GlobalFeed(LoginRequiredMixin, View, PaginatedViewMixin):
    """Class view used to generate a paginated list of all tickets and reviews
    ordered chronologically (soonest first)
    """
    template_name = 'home.html'

    def get(self, request):
        """
        argument: GET request
        return: url + page_object (= paginated posts)
        """
        reviews = models.Review.objects.all()
        tickets = models.Ticket.objects.all()
        posts_paged = self.paginate_view(
            request, sorted(chain(reviews, tickets),
                            key=lambda x: x.time_created, reverse=True))
        return render(request, self.template_name,
                      context={'page_obj': posts_paged})


class UserFeed(LoginRequiredMixin, View, PaginatedViewMixin):
    """Class view used to generate a paginated list of the logged user
        tickets and reviews
        """
    template_name = 'user_feed.html'

    def get(self, request):
        """
        argument: GET request
        return: url + page_object (= paginated posts)
        """
        reviews = models.Review.objects.filter(user_id=request.user)
        tickets = models.Ticket.objects.filter(user_id=request.user)
        posts_paged = self.paginate_view(
            request, sorted(chain(reviews, tickets),
                            key=lambda x: x.time_created, reverse=True))
        return render(request, self.template_name,
                      context={'page_obj': posts_paged})


# -----------------------------TICKET-----------------------------#

class TicketListView(ListView, PaginatedViewMixin):
    """Generic ClassBasedView used to generate a paginated list of all tickets
       actually used on ticket_feed.html and ticket_unchecked_feed.html
        """
    model = models.Ticket
    template_name = ''

    def get_context_data(self, **kwargs):
        """
        argument: GET request
        return: url + page_object (= paginated posts)
        """
        context = super().get_context_data(**kwargs)
        tickets = self.get_queryset().order_by('time_created').reverse()
        tickets_paged = self.paginate_view(self.request, tickets)
        context['page_obj'] = tickets_paged
        return context


@login_required
def ticket_create(request):
    """Create ticket through TicketForm

    argument: request
    return: GET: url + form
            POST: a new ticket saved """

    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    return render(request, 'ticket/ticket_create.html', context={'form': form})


@login_required
def ticket_edit(request, ticket_id):
    """Edit ticket through TicketForm

    argument: request + ticket_id to edit
    return: GET: url + ticket_object + TicketForm
            POST: edited ticket saved """

    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        edit_form = forms.TicketForm(request.POST, instance=ticket)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('home')
    return render(request, 'ticket/ticket_edit.html',
                  context={'ticket': ticket, 'edit_form': edit_form})


@login_required
def ticket_delete(request, ticket_id):
    """Delete ticket through DeleteForm

    argument: request + ticket_id to delete
    return: GET: url + ticket_object + DeleteForm
            POST: delete ticket """

    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    delete_form = forms.DeleteBlogForm()
    if request.method == 'POST':
        ticket.delete()
        return redirect('home')
    context = {'delete_form': delete_form,
               'ticket': ticket, }
    return render(request, 'ticket/ticket_delete.html', context=context)


@login_required
def ticket_view(request, ticket_id):
    """View ticket selected

        argument: request + ticket_id to view
        return: GET: url + ticket_object """

    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(request, 'ticket/ticket_view.html',
                  context={'ticket': ticket})


# -----------------------------REVIEW-----------------------------#

class ReviewListView(ListView, PaginatedViewMixin):
    """Generic ClassBasedView used to generate a paginated list of all reviews
        """
    model = models.Review
    template_name = 'review/review_feed.html'

    def get_context_data(self, **kwargs):
        """
        argument: GET request
        return : url + page_object (= paginated posts)
        """
        context = super(ReviewListView, self).get_context_data(**kwargs)
        reviews = self.get_queryset().order_by('time_created').reverse()
        reviews_paged = self.paginate_view(self.request, reviews)
        context['page_obj'] = reviews_paged
        return context


@login_required
def review_and_ticket_creation(request):
    """Create a review without a ticket base
    create both review and ticket through ReviewFrom and TicktForm

    argument : request
    return: GET: url + ReviewForm + TicketForm
            POST: a new ticket saved + new request saved
                + adding a review_associated to the ticket"""

    review_form = forms.ReviewForm()
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if all([review_form.is_valid(), ticket_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.review_associated = True
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    context = {
        'review_form': review_form,
        'ticket_form': ticket_form,
    }
    return render(request, 'review/review_and_ticket_creation.html',
                  context=context)


@login_required
def review_on_existing_ticket(request, ticket_id):
    """Create a review on a ticket base, through ReviewFrom

    argument: request
    return: GET: url + ReviewForm + ticket_object
            POST: a new request saved
                + adding a review_associated to the ticket"""

    review_form = forms.ReviewForm()
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        if all([review_form.is_valid()]):
            ticket.review_associated = True
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    context = {
        'review_form': review_form,
        'ticket': ticket,
    }
    return render(request, 'review/review_on_existing_ticket.html',
                  context=context)


@login_required
def review_edit(request, review_id):
    """Edit a review through ReviewForm

    argument: request + review_id to edit
    return: GET: url + review_object + ReviewForm
            POST: edited review saved """

    review = get_object_or_404(models.Review, id=review_id)
    edit_form = forms.ReviewForm(instance=review)
    if request.method == 'POST':
        edit_form = forms.ReviewForm(request.POST, instance=review)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('home')
    context = {'review': review, 'edit_form': edit_form}
    return render(request, 'review/review_edit.html', context=context)


@login_required
def review_delete(request, review_id):
    """Delete review through DeleteForm
    Does not delete the ticket associated

    argument: request + review to delete
    return: GET: url + review_object + DeleteForm
            POST: delete review
            + unchecking review_associated to the ticket"""

    review = get_object_or_404(models.Review, id=review_id)
    delete_form = forms.DeleteBlogForm()
    if request.method == 'POST':
        review.delete()
        review.ticket.review_associated = False
        review.ticket.save()
        return redirect('home')
    context = {'review': review, 'delete_form': delete_form}
    return render(request, 'review/review_delete.html', context=context)


@login_required
def review_view(request, review_id):
    """View review selected

        argument: request + review_object to view
        return: GET: url + review_object """

    review = get_object_or_404(models.Review, id=review_id)
    return render(request, 'review/review_view.html',
                  context={'review': review})

# -----------------------------FOLLOWED USERS-----------------------------#


@login_required
def follow_users_page(request):
    """View with :
        - a submit button to follow an existing user
        - a followed users list (with a button to unfollow for each)
        - a following users list

        users_followed and following_users are treated through
        UserFollows object (relation between two users with their id), linked
        to User.subscriptions

        argument: request
        return: GET: url + all users_followed_object
                POST: add a followed user (create a UserFollows)"""

    if request.method == 'POST':
        for values in User.objects.all():
            if request.POST['query'] == values.username:
                followed_user = values
                test = models.UserFollows()
                print(test)
                test.user = request.user
                test.followed_user = followed_user
                test.save()
                print(test)
        return redirect('follow_users_page')
    users_followed = models.UserFollows.objects.all()
    context = {'users_followed': users_followed}
    return render(request, 'followed_users/follow_users_page.html',
                  context=context)


@login_required
def user_unfollow_page(request, user_follows_id):
    """Followed_user view with an "unfollow option" (DeleteForm)
    and all posts related to this user

    argument: request, followed_user_id
    return: GET: url + user_followed_object + posts of this user + DeleteFrom
            POST: unfollow the user (delete the UserFollows object)"""

    user_followed = get_object_or_404(models.UserFollows, id=user_follows_id)
    reviews = models.Review.objects.filter(
        user_id=user_followed.followed_user_id)
    tickets = models.Ticket.objects.filter(
        user_id=user_followed.followed_user_id)
    posts_paged = sorted(chain(reviews, tickets),
                         key=lambda x: x.time_created, reverse=True)
    delete_form = forms.DeleteBlogForm()
    if request.method == 'POST':
        user_followed.delete()
        return redirect('follow_users_page')
    context = {'user_followed': user_followed, 'page_obj': posts_paged,
               'delete_form': delete_form}
    return render(request, 'followed_users/user_unfollow_page.html',
                  context=context)


class FollowedFeed(LoginRequiredMixin, View, PaginatedViewMixin):
    """Class view used to generate a paginated list of all followed_users
    tickets and reviews, ordered chronologically (soonest first)
        """
    template_name = 'followed_users/followed_feed.html'

    def get(self, request):
        """
        argument: GET request
        return: url + page_object (= paginated posts)
        """
        reviews = models.Review.objects.filter(
            user__in=request.user.subscriptions.all())
        tickets = models.Ticket.objects.filter(
            user__in=request.user.subscriptions.all())
        posts_paged = self.paginate_view(
            request, sorted(chain(reviews, tickets),
                            key=lambda x: x.time_created, reverse=True))
        return render(request, self.template_name,
                      context={'page_obj': posts_paged})
