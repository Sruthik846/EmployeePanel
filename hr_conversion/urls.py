from django.urls import path,include
from . import views  
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
   # ------ conversion ------ #
   path('',views.home,name='hr-home'),
   path('emp-upload', views.upload_EMPFile, name='emp-upload'),
   path('add-annotator', views.add_ANNOTATOR, name='add-annotator'),
   path('add-coordinator', views.add_COORDINATOR, name='add-coordinator'),
   path('add-hrteam', views.add_HRteam, name='add-hrteam'),
   path('delete-emp/<str:pk>', views.del_EMP, name='del-emp'),
   path('convert', views.conversion, name='convert'),
   path('edit-employee/<str:pk>',views.edit_employee,name='edit-employee'),
   path('add-technical', views.add_TECHNICAL, name='add-technical'),
   path('export-emp',views.export_EMPfile,name='export-emp'),
#    path('dwnld', views.downloadMerged, name='dwnld'),


] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
