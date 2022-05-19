from itertools import chain

from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.forms import formset_factory
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render

from django.views.generic import TemplateView, View, DetailView
from django.utils.decorators import method_decorator

from . import forms, models
# from authentication.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class GlobalFeed(LoginRequiredMixin, View):
    template_name = ''

    def get(self, request):
        reviews = models.Review.objects.all()
        tickets = models.Ticket.objects.all()
        posts = sorted(chain(reviews, tickets), key=lambda x: x.time_created, reverse=True)
        posts_paged = Paginator(posts, 6).get_page(request.GET.get('page'))
        tickets_paged = Paginator(tickets, 6).get_page(request.GET.get('page'))
        reviews_paged = Paginator(reviews, 6).get_page(request.GET.get('page'))
        context = {'posts_paged': posts_paged, 'tickets_paged': tickets_paged, 'reviews_paged': reviews_paged}
        return render(request, self.template_name, context=context)


class FollowedFeed(LoginRequiredMixin, View):
    template_name = ''

    def get(self, request):
        reviews = models.Review.objects.filter(user__in=request.user.abonnements.all())
        tickets = models.Ticket.objects.filter(user__in=request.user.abonnements.all())
        posts = sorted(chain(reviews, tickets), key=lambda x: x.time_created, reverse=True)
        posts_paged = Paginator(posts, 6).get_page(request.GET.get('page'))
        tickets_paged = Paginator(tickets, 6).get_page(request.GET.get('page'))
        reviews_paged = Paginator(reviews, 6).get_page(request.GET.get('page'))
        context = {'posts_paged': posts_paged, 'tickets_paged': tickets_paged, 'reviews_paged': reviews_paged}
        return render(request, self.template_name, context=context)


class TicketCreate(LoginRequiredMixin, View):
    template_name = ''

    def get(self, request):
        form = forms.TicketForm()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = forms.TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')


class TicketViewAndEdit(LoginRequiredMixin, View):
    template_name = ''
    ticket_id = ''
    if ticket_id != '':
        ticket = get_object_or_404(models.Ticket, id=ticket_id)

    def get(self, request):
        edit_form = forms.TicketForm(instance=self.ticket)
        context= {'ticket': self.ticket, 'edit_form':edit_form}
        return render(request, self.template_name, context=context)

    def post(self, request):
        edit_form = forms.TicketForm(request.POST, instance=self.ticket)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('home')



class ReviewCreate(LoginRequiredMixin, View):
    template_name = ''
    ticket_id = ''
    if ticket_id != '':
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
    form = forms.ReviewForm()

    def get(self, request):
        context = {'form' : self.form, 'ticket' : self.ticket}
        return render(request, self.template_name, context=context)

    def post(self, request):
        review_form = forms.ReviewForm(request.POST)
        if self.ticket_id != '':
            ticket_form = forms.TicketForm(request.POST, request.FILES)
            if ticket_form.is_valid():
                ticket = ticket_form.save(commit=False)
                ticket.user = request.user
                ticket.review_done()
                ticket.save()
        if review_form.is_valid():
            self.ticket.review_associated = True
            self.ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = self.ticket
            review.save()
            return redirect('home')


class ReviewViewAndEdit(LoginRequiredMixin, View):
    template_name = ''
    review_id = ''
    if review_id != '':
        review = get_object_or_404(models.Review, id=review_id)

    def get(self, request):
        edit_form = forms.ReviewForm(instance=self.review)
        context= {'ticket': self.review, 'edit_form': edit_form}
        return render(request, self.template_name, context=context)

    def post(self, request):
        edit_form = forms.ReviewForm(request.POST, instance=self.review)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('home')





class DeleteView(LoginRequiredMixin, View):
    template_name = ''
    review_id = ''
    ticket_id = ''
    if review_id != '':
        review = get_object_or_404(models.Review, id=review_id)
    if ticket_id != '':
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
    delete_form = forms.DeleteBlogForm()

    def get(self, request):
        context = {'ticket': self.ticket, 'review': self.review, 'delete_form': self.delete_form}
        return render(request, 'review/review_delete.html', context=context)

    def post(self, request):
        self.ticket.delete()
        return redirect('home')

    def delete_review(self, request):
        self.review.delete()
        self.review.ticket.review_associated = False
        self.review.ticket.save()
        return redirect('home')


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
def follow_users(request):
    followed_form = forms.UserFollowsForm()
    if request.method == 'POST':
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
        form = forms.UserFollowsForm(request.POST, instance=request.user)
        followed_form = forms.UserFollowsForm(request.POST, instance=request.user)
        if followed_form.is_valid():
            followed_form.save()
            return redirect('users_followed_feed')
    users_followed = models.UserFollows.objects.all()
    context = {'followed_form': followed_form, 'users_followed': users_followed}
    return render(request, 'users_followed_feed.html', context=context)


# @login_required
# def posts(request):
#     form = forms.FollowUsersForm(request.POST, instance=request.user)
#     return render(request, 'review/posts.html', context={'form': form})

# @login_required
# def user_delete (request, user_follows_id):
#     user_followed = models.UserFollows.objects.all()
#     user_followed = get_object_or_404(models.UserFollows, id=user_follows_id)
#     user_follows = user_followed.followed_user
#     reviews = models.Review.objects.filter(user__in=request.user.abonnements.all())
#     delete_form = forms.DeleteBlogForm()
#     if request.method == 'POST':
#         user_followed.delete()
#         return redirect('home')
#     context = {'user_followed': user_followed, 'user_follows': user_follows, 'posts': posts, 'delete_form': delete_form}
#     return render(request, 'user_delete.html', context=context)



class FilmBaseView(View):
    model = Film
    fields = '__all__'
    success_url = reverse_lazy('films:all')

class FilmListView(FilmBaseView, ListView):
    """View to list all films.
    Use the 'film_list' variable in the template
    to access all Film objects"""

class FilmDetailView(FilmBaseView, DetailView):
    """View to list the details from one film.
    Use the 'film' variable in the template to access
    the specific film here and in the Views below"""

class FilmCreateView(FilmBaseView, CreateView):
    """View to create a new film"""

class FilmUpdateView(FilmBaseView, UpdateView):
    """View to update a film"""

class FilmDeleteView(FilmBaseView, DeleteView):
    """View to delete a film"""

