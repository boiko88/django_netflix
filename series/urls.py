from django.urls import path
from series.views import HomePageView, TestPageView, CustomLogoutView, create_anime, update_anime, delete_anime, anime_search, register, sign_in


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('test/', TestPageView.as_view(), name='test'),
    path('create/', create_anime, name='create_anime'),
    path('update/<int:pk>/', update_anime, name='update_anime'),
    path('delete/<int:pk>/', delete_anime, name='delete_anime'),
    path('search/', anime_search, name='anime_search'),
    path('register/', register, name='register'),
    path('sign_in/', sign_in, name='sign_in'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
