from django.urls import path
from . import views  

urlpatterns = [
   path('',views.addsalaryMonth,name='salaryhome'),
   path('<str:year>/<str:month>/files',views.viewSalaryFiles,name='viewslfiles'),
   path('<str:year>/<str:month>',views.idSalaryDetails,name='viewsalary'),
   path('<str:year>/<str:month>/delsalary',views.delSalary,name='del-salary'),
   path('uploadsalary/<str:year>/<str:month>',views.uploadSalaryFile2,name='upload-salary'),

   # path('uploadsalary/<str:year>/<str:month>',views.uploadSalaryFile,name='upload-salary-file'),
   # path('uploaddata/<str:year>/<str:month>',views.uploadSalaryData,name='upload-data'), 

   path('<str:year>/<str:month>/add-salary',views.add_id_salary,name='add-salary'),
   path('<str:year>/<str:month>/<str:ifid>/view',views.idSalary,name='view-ifsalary'),
   path('<str:year>/<str:month>/<int:ifid>/del',views.del_id_salary,name='del-idsalary'),
   path('<str:year>/<str:month>/<str:ifid>/edit-basic',views.editBasicSalary,name='edit-basic'),
   path('<str:year>/<str:month>/<str:ifid>/edit-special',views.editSpecialIncome,name='edit-special'), 
   path('<str:year>/<str:month>/<str:ifid>/edit-deduction',views.editDeductions,name='edit-deduction'),
   path('<str:year>/<str:month>/<str:ifid>/edit-grandtotal',views.editGrandTotal,name='edit-grandtotal'),

   path('emp/salary/',views.id_salaryhome,name='idsalary'),
   path('emp/salary/<str:year>/<str:month>/',views.id_salaryData,name='idsalarydata'),   

]