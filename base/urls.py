from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<int:pk>/',views.room,name='room-page'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>', views.deleteRoom, name='delete-room'),
    path('login/', views.loginPage, name='login-page'),
    path('register/', views.registerPage, name='register-page'),
    path('logout/', views.logoutPage, name='logout-page'),
    path('delete-message/<str:pk>', views.deletMessage, name='delete-message'),
    path('profile/<str:pk>',views.userProfile,name='user-profile'),
    path('update-user/',views.updateUser,name='update-user'),
    path('topics/',views.topicPage,name='topics-page'),
    path('activity/',views.activityPage,name='activity-page'),
]
