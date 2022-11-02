from django.urls import path  
from . import views        

urlpatterns = [
    path('monthData/',views.addMonth,name='addmonth'),
    path('delete_month/<str:pk>',views.delMonth, name='delmonth'),
    path('viewfile/<str:year>/<str:month>',views.viewPnFiles,name='viewfiles'),
    path('punchingdetails/<str:year>/<str:month>',views.PunchTable, name='viewpunchings'),  
    path('uploadPunching/<str:year>/<str:month>',views.uploadPunching2,name='uploadPunch'),  

    # path('uploadPunchFile/<str:year>/<str:month>',views.uploadPunchingFile,name='uploadPunchFile'),
    # path('uploadPunchData/<str:year>/<str:month>',views.uploadPunchingData,name='uploadPunchData'),

    path('delete_file/<str:year>/<str:month>/<str:file_id>',views.delPunchFile, name='delPunchFile'),
    path('ifidPunching/<str:pk>',views.ifidPunching, name='ifidpunching'),
    path('expPunching',views.punchTableExport, name='punchingexport'),
    path('punchingdetails/<str:year>/<str:month>/<str:ifid>/update',views.editPunching, name='edit-punching'),

   
    path('home/',views.punchingHome,name='pnhome'),
    path('emp/punchingdata/<str:year>/<str:month>/',views.id_punching,name='idpunching'),
    path('emp/punchingdata/<str:year>/<str:month>/punchings/',views.id_DayData,name='punchings'),    
]