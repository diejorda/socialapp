from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('settings/',views.settings, name='settings'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('post/', views.post, name='post'),
    path('like/', views.like, name='like'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('follow/', views.follow, name='follow'),
    path('search/', views.search, name='search'),
    path('comment/', views.comment, name='comment')
]