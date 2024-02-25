from decimal import Decimal

from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404,redirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.urls import reverse

from movies.forms import CommentForm, RatingForm
from movies.models import Category, Movie, Comment, Rating


# Create your views here.

def all_movies_category(request, c_slug=None):

    c_page=None
    movies_list=None
    if c_slug is not None:
        c_page = get_object_or_404(Category, slug=c_slug)
        movies_list = Movie.objects.filter(category=c_page)
    else:
        movies_list = Movie.objects.all()
    paginator = Paginator(movies_list, 6)
    try:
        page_num = int(request.GET.get('page', '1'))
    except:
        page_num=1
    try:
        movies = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        movies = paginator.page(paginator.num_pages)
    return render(request, 'category.html', {'category':c_page, 'movies':movies})


def movies_category_detail(request, c_slug, m_slug):
    try:
        movie=Movie.objects.get(category__slug=c_slug, slug=m_slug)
    except Exception as e:
        raise e

    comments = Comment.objects.filter(movie=movie)
    ratings = Rating.objects.filter(movie=movie)
    average_rating = Rating.objects.filter(movie=movie).aggregate(avg_rating=Avg('value'))['avg_rating']
    if average_rating:
        average_rating = Decimal(average_rating).quantize(Decimal('0.1'))

    if request.method == 'POST' and request.user.is_authenticated:
        if 'comment' in request.POST:
            new_comment = Comment.objects.create(movie=movie, user=request.user, content=request.POST.get('comment'))
            new_comment.save()
        if 'rating' in request.POST:
            if Rating.objects.filter(movie=movie, user=request.user).exists():
                old_rating = Rating.objects.get(movie=movie, user=request.user)
                new_value = request.POST.get('rating')
                old_rating.value = new_value
                old_rating.save()
                # messages.error(request, "You have already rated this post.")
            else:
                new_rating = Rating.objects.create(movie=movie, user=request.user, value=request.POST.get('rating'))
                new_rating.save()

        movie.save()
        return redirect(reverse('movies:movies_category_detail', args=[movie.category.slug, movie.slug]))

    return render(request, 'movie.html', {'movie': movie, 'comments':comments, 'ratings':ratings, 'average_rating':average_rating, 'stars_range':range(1,6)})