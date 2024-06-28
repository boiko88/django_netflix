from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

from datetime import datetime
import csv

from . models import Anime
from . forms import AnimeForm, RegistrationForm, SignInForm


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            animes = Anime.objects.filter(user=self.request.user)
        else:
            animes = Anime.objects.none()
        context['animes'] = animes
        return context
    

class TestPageView(TemplateView):
    template_name = 'test_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animes = Anime.objects.all()
        context['animes'] = animes
        context['form'] = AnimeForm()
        return context


# This function writes all the changes in a CSV file
def log_to_csv(action_phrase, file_name='user_log.csv'):
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")
    time_string = now.strftime("%H:%M:%S")

    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([action_phrase, date_string, time_string])
        print('The data has been added successfully to', file_name)

# CRUD for Anime


@login_required(login_url='sign_in')
def create_anime(request):
    if request.method == 'POST':
        form = AnimeForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            messages.info(request, 'Anime created')
            log_to_csv('An anime element has been created')
            return redirect('home')
        else:
            form.clean()
    else:
        form = AnimeForm()
    return render(request, 'create_anime.html', {'form': form})


@login_required(login_url='sign_in')
def update_anime(request, pk):
    anime = get_object_or_404(Anime, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AnimeForm(request.POST, instance=anime)
        if form.is_valid():
            form.save()
            messages.info(request, 'Anime was updated')
            log_to_csv('An anime element has been updated')
            return redirect('home')
    else:
        form = AnimeForm(instance=anime)
    return render(request, 'update_anime.html', {'form': form})


@login_required(login_url='sign_in')
def delete_anime(request, pk):
    anime = get_object_or_404(Anime, pk=pk, user=request.user)
    anime.delete()
    log_to_csv('An anime element has been deleted')
    messages.info(request, 'Anime was deleted')
    return redirect('home')


class AnimeSearchView(ListView):
    model = Anime
    template_name = 'anime_search.html'
    context_object_name = 'animes'
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        anime_list = Anime.objects.filter(user=self.request.user, eng_name__contains=query)
        return anime_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.object_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            animes = paginator.page(page)
        except PageNotAnInteger:
            animes = paginator.page(1)
        except EmptyPage:
            animes = paginator.page(paginator.num_pages)
        context['animes'] = animes
        return context


# Search
def anime_search(request):
    query = request.GET.get('query')
    release_year = request.GET.get('release_year')

    if query:
        try:
            release_year = int(query)
            animes = Anime.objects.filter(release_year=release_year)
        except ValueError:
            animes = Anime.objects.filter(Q(eng_name__icontains=query) | Q(director_name__icontains=query))
    else:
        animes = Anime.objects.all()

    context = {'animes': animes}
    return render(request, 'anime_search.html', context)


# Registration
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful. Welcome!')
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


# Sign in
def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            messages.info(request, 'Signing in was successful!.')
            login(request, user)
            return redirect('home')
    else:
        form = SignInForm()
    return render(request, 'sign_in.html', {'form': form})


# Logout
class CustomLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('home')
