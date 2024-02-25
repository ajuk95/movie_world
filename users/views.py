from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render, redirect
from django.urls import reverse

from movies.models import Movie, Category
from users.forms import MovieForm, UserForm


# Create your views here.
def add_movie(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('users:view_profile', args=[request.user.username]))  # Redirect to a success URL
    else:
        form = MovieForm(user=request.user)
    return render(request, 'add_movie.html', {'form': form,'categories': categories})

def edit_movie(request, m_slug):
    movie = Movie.objects.get(slug=m_slug)
    # print('movie =', movie)
    # movie = Movie.objects.get(id=id)
    form = MovieForm(request.POST or None, request.FILES, instance=movie, user=request.user)
    print('error =', form.errors)
    # print('form =', form)
    if form.is_valid():
        form.save()
        return redirect(reverse('users:view_profile', args=[request.user.username]))

    return render(request, 'edit_movie.html', {'form': form, 'movie': movie})
    # return render(request, 'edit_movie.html', {'movie':movie})

def delete_movie(request, m_slug):
    movie = Movie.objects.get(slug=m_slug)
    if request.method == 'POST':
        movie.delete()
        return redirect(reverse('users:view_profile', args=[request.user.username]))
    return render(request, 'delete_movie.html', {'movie':movie})

def view_profile(request, c_slug):
    user = User.objects.get(username=c_slug)
    movies_list = Movie.objects.filter(uploaded_by=user)
    paginator = Paginator(movies_list, 6)
    try:
        page_num = int(request.GET.get('page', '1'))
    except:
        page_num=1
    try:
        movies_uploaded = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        movies_uploaded = paginator.page(paginator.num_pages)
    return render(request, 'view_profile.html', {'user':user, 'movies_uploaded':movies_uploaded})

def edit_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('users:view_profile', args=[request.user.username]))
    else:
        form = UserForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form':form})
