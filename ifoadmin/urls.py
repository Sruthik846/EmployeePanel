from django.urls import path  
from . import views        

urlpatterns = [
    path('home/', views.home, name='home'),
    path('usersdetails/', views.userpage, name='userpage'),
    path('users/',views.viewUsers, name='users'),
    path('deleteuser/<str:pk>',views.delUser, name='deleteuser'),
    path('usercreds/',views.employeeCred, name='usercred'),
    path('uploadcreds/', views.uploadcred, name='uploadcred'),
    path('deletecred/<str:pk>',views.deletecred, name='deletecred'),
    path('updatecred/<str:pk>',views.updateMobile, name='updatemobile'),
]