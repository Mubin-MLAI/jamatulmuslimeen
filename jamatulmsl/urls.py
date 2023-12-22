from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('addResume', views.savepersondetails.as_view(), name = 'addResume'),
    path('signup', views.signupPage, name='signupPage'),
    path('login', views.loginPage, name='loginPage'),
    path('logout', views.logoutPage, name='logoutPage'),
    path('listResume', views.listResume.as_view(), name='listResume'),
    path('viewResume', views.viewResume.as_view(), name='viewResume'),
    path('updateapplicant', views.updateapplicant.as_view(), name='updateapplicant'),
]