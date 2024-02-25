from django.urls import path

from movies import views
app_name = 'movies'

urlpatterns = [
    path('', views.all_movies_category, name='all_movies_category'),
    path('<slug:c_slug>/', views.all_movies_category, name='movies_by_category'),
    path('<slug:c_slug>/<slug:m_slug>/', views.movies_category_detail, name='movies_category_detail')
]