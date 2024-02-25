from django.urls import path

from . import views
app_name = 'users'

urlpatterns = [
    # path('', views.view_profile, name='view_profile'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('edit_movie/<slug:m_slug>/', views.edit_movie, name='edit_movie'),
    path('delete_movie/<slug:m_slug>/', views.delete_movie, name='delete_movie'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('<slug:c_slug>/', views.view_profile, name='view_profile'),
    # path('<slug:c_slug>/<slug:m_slug>/', views.moviesDetail, name='movies_category_detail')
]