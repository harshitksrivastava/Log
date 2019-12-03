from django.urls import path
from .import views

urlpatterns = [
    path('',views.HomePage.as_view(),name='homepage'),
    path('signup/',views.SignUp.as_view(),name='signup'),
    path('login/',views.Login.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('api/',views.ProfileList.as_view(),name='loginapi'),
]
