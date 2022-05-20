from itertools import chain

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.shortcuts import get_object_or_404, redirect, render

from django.views import View
from django.views.generic.list import ListView

from django.urls import reverse_lazy

from . import forms, models


User = get_user_model()


# -----------------------------MIXINS-----------------------------#

class PaginatedViewMixin:

    @staticmethod
    def paginate_view(request, object_paginated):
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
    template_name = ''

    def get(self, request):
        reviews = models.Review.objects.all()
        tickets = models.Ticket.objects.all()
        posts_paged = self.paginate_view(
            request, sorted(chain(reviews, tickets),
                            key=lambda x: x.time_created, reverse=True))
        return render(request, self.template_name,
                      context={'page_obj': posts_paged})


# -----------------------------TICKET-----------------------------#

class TicketBaseView(LoginRequiredMixin, View):
    model = models.Ticket
    form_class = forms.TicketForm
    success_url = reverse_lazy('home')


class TicketListView(ListView, TicketBaseView, PaginatedViewMixin):
    model = models.Ticket
    template_name = ''
    answered_tickets = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tickets = self.get_queryset().order_by('time_created').reverse()
        tickets_paged = self.paginate_view(self.request, tickets)
        context['page_obj'] = tickets_paged
        return context


@login_required
def ticket_create(request):
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
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(request, 'ticket/ticket_view.html',
                  context={'ticket': ticket})


# -----------------------------REVIEW-----------------------------#

class ReviewBaseView(LoginRequiredMixin, View):
    model = models.Review
    form_class = forms.ReviewForm
    success_url = reverse_lazy('home')


class ReviewListView(ListView, ReviewBaseView, PaginatedViewMixin):
    model = models.Review
    template_name = ''

    def get_context_data(self, **kwargs):
        context = super(ReviewListView, self).get_context_data(**kwargs)
        reviews = self.get_queryset().order_by('time_created').reverse()
        reviews_paged = self.paginate_view(self.request, reviews)
        context['page_obj'] = reviews_paged
        return context


@login_required
def review_and_ticket_creation(request):
    review_form = forms.ReviewForm()
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if all([review_form.is_valid(), ticket_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.review_done()
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
    review = get_object_or_404(models.Review, id=review_id)
    delete_form = forms.DeleteBlogForm()
    if request.method == 'POST':
        review.delete()
        review.ticket.review_associated = False
        review.ticket.save()
        return redirect('home')
    context = {'review': review, 'delete_form': delete_form}
    return render(request, 'review/review_delete.html', context=context)


# -----------------------------FOLLOWED USERS-----------------------------#


@login_required
def follow_users_page(request):
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
    user_followed = get_object_or_404(models.UserFollows, id=user_follows_id)
    reviews = models.Review.objects.all()
    tickets = models.Ticket.objects.all()
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
    template_name = 'followed_users/followed_feed.html'

    def get(self, request):
        reviews = models.Review.objects.filter(
            user__in=request.user.abonnements.all())
        tickets = models.Ticket.objects.filter(
            user__in=request.user.abonnements.all())
        posts_paged = self.paginate_view(
            request, sorted(chain(reviews, tickets),
                            key=lambda x: x.time_created, reverse=True))
        return render(request, self.template_name,
                      context={'page_obj': posts_paged})
