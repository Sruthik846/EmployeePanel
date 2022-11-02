from django.urls import path
from . import views  

urlpatterns = [
   path('',views.messageHome,name='messagehome'),
   path('addmessage',views.addMessage,name='add_message'),
   path('delete-mg/<str:pk>',views.deleteMessage,name='delete_message'),
   path('edit-mg/<str:pk>',views.editMessage,name='edit_message'),
   path('uploader_save/',views.file_upload_save,name='uploader-save'),

   path('emp/message/', views.id_notifications, name='msgHome'),
   path('emp/message/<str:title>/', views.msgReadmore, name='msgdetails'),
]