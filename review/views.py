from itertools import chain

from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.forms import formset_factory
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from . import forms, models


@login_required
def home(request):
    reviews = models.Review.objects.all()
    tickets = models.Ticket.objects.all()
    posts = sorted(chain(reviews, tickets), key=lambda x: x.time_created, reverse=True)
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'home.html', context=context)

@login_required
def user_feed(request):
    reviews = models.Review.objects.all()
    tickets = models.Ticket.objects.all()
    posts = sorted(chain(reviews, tickets), key=lambda x: x.time_created, reverse=True)
    return render(request, 'user_feed.html', context={'posts': posts})

@login_required
def followed_feed(request):
    reviews = models.Review.objects.filter(user__in=request.user.abonnements.all())
    tickets = models.Ticket.objects.filter(user__in=request.user.abonnements.all())
    posts = sorted(chain(reviews, tickets), key=lambda x: x.time_created, reverse=True)
    return render(request, 'followed_feed.html', context={'posts': posts})


@login_required
def ticket_create(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            # set the uploader to the user before saving the model
            ticket.user = request.user
            # now we can save
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
    return render(request, 'ticket/ticket_edit.html', context={'edit_form': edit_form})


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
    return render(request, 'ticket/ticket_view.html', context={'ticket': ticket})


@login_required
def ticket_feed(request):
    tickets = models.Ticket.objects.all()
    return render(request, 'ticket/ticket_feed.html', context={'tickets': tickets})

@login_required
def ticket_unchecked_feed(request):
    tickets = models.Ticket.objects.all()
    return render(request, 'ticket/ticket_unchecked_feed.html', context={'tickets': tickets})


@login_required
def review_create(request):
    form = forms.ReviewForm()
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            # set the uploader to the user before saving the model
            review.user = request.user
            # now we can save
            review.save()
            return redirect('home')
    return render(request, 'review/review_create.html', context={'form': form})


@login_required
def review_view(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    return render(request, 'review/review_view.html', context={'review': review})


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


@login_required
def review_feed(request):
    reviews = models.Review.objects.all()
    return render(request, 'review/review_feed.html', context={'reviews': reviews})


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
    return render(request, 'review/review_and_ticket_creation.html', context=context)


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
    return render(request, 'review/review_on_existing_ticket.html', context=context)


# @login_required
# def follow_users(request):
#     form = forms.FollowUsersForm(instance=request.user)
#     followed = forms.FollowUsersForm(instance=request.user)
#     followers = request.user.follows.all()
#     if request.method == 'POST':
#         form = forms.FollowUsersForm(request.POST, instance=request.user)
#         followed = forms.UserFollowsForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             # followed.save()
#             return redirect('home')
#     context = {'form': form, 'followed': followed, 'followers': followers}
#     return render(request, 'follow_users.html', context=context)


@login_required
def follow_users(request):
    followed_form = forms.UserFollowsForm(instance=request.user)
    if request.method == 'POST':
        # form = forms.FollowUsersForm(request.POST, instance=request.user)
        followed_form = forms.UserFollowsForm(request.POST, instance=request.user)
        if followed_form.is_valid():
            followed_form.save()
            return redirect('follow_users')
    context = {'followed_form': followed_form}
    return render(request, 'follow_users.html', context=context)


@login_required
def users_followed_feed(request):
    followed_form = forms.UserFollowsForm(instance=request.user)
    if request.method == 'POST':
        # form = forms.FollowUsersForm(request.POST, instance=request.user)
        followed_form = forms.UserFollowsForm(request.POST, instance=request.user)
        if followed_form.is_valid():
            followed_form.save()
            return redirect('users_followed_feed')
    if request.method == 'GET':  # If the form is submitted
        search_query = request.GET.get('search_box', None)

    users_followed = models.UserFollows.objects.all()
    context = {'followed_form': followed_form, 'users_followed': users_followed}
    return render(request, 'users_followed_feed.html', context=context)


def posts(request):
    form = forms.FollowUsersForm(request.POST, instance=request.user)
    return render(request, 'review/posts.html', context={'form': form})

def user_delete (request, user_follows_id):
    user_followed = models.UserFollows.objects.all()
    user_followed = get_object_or_404(models.UserFollows, id=user_follows_id)
    user_follows = user_followed.followed_user
    reviews = models.Review.objects.filter(user__in=request.user.abonnements.all())
    # tickets = models.Ticket.objects.filter(user=user_id)
    # posts = sorted(chain(reviews, tickets), key=lambda x: x.time_created, reverse=True)
    delete_form = forms.DeleteBlogForm()
    if request.method == 'POST':
        user_followed.delete()
        return redirect('home')
    context = {'user_followed': user_followed, 'user_follows': user_follows, 'posts': posts, 'delete_form': delete_form}
    return render(request, 'user_delete.html', context=context)

@login_required
def specific_user_delete(request,user_id):
    reviews = models.Review.objects.all()
    tickets = models.Ticket.objects.all()
    posts = sorted(chain(reviews, tickets), key=lambda x: x.time_created, reverse=True)
    return render(request, 'user_feed.html', context={'posts': posts})
# user_searched = models.UserFollows.objects.filter(
#         Q(contributors__in=request.user.follows.all()) | Q(starred=True))


# def followToggle(request, author):
#     authorObj = User.objects.get(username=author)
#     currentUserObj = User.objects.get(username=request.user.username)
#     following = authorObj.following.all()
#
#     if author != currentUserObj.username:
#         if currentUserObj in following:
#             authorObj.following.remove(currentUserObj.id)
#         else:
#             authorObj.following.add(currentUserObj.id)
#
#     return HttpResponseRedirect(reverse(profile, args=[authorObj.username]))