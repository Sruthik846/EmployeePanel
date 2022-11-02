
import csv
from datetime import datetime
from io import BytesIO, StringIO
import zipfile
import textwrap
from django.http import HttpResponse
from django.shortcuts import redirect, render
from hr_conversion.models import EmployeeFile, EmployeeList
import os, shutil
import pandas as  pd
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_users
import xlwt
# Create your views here.


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin','hrteam'])
def home(request):
    empfile = None
    if EmployeeFile.objects.all().exists():
        empfile = EmployeeFile.objects.all().latest("id")
        empfile.name = str(empfile.employee_file).split("/")[-1]
    crdntrs = EmployeeList.objects.filter(designation='co-ordinators')
    annotrs = EmployeeList.objects.filter(designation='annotators')
    hrteam = EmployeeList.objects.filter(designation='hrteam')
    context = {"page_title":"HR Conversion","emp_file":empfile,
                'coordinators':crdntrs ,'annotators':annotrs, 'hrteam':hrteam
                }
    return render(request, 'hr_home.html' , context)

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin','hrteam'])
def upload_EMPFile(request):
    if request.method == "POST":
        # EmployeeFile.objects.all().delete()
        # EmployeeList.objects.all().delete()
        path = os.getcwd()
        # try:
        #     shutil.rmtree(os.path.join(path,'media/conversion/emp'))
        # except:
        #     pass
        emp_file = request.FILES.get('emp-file')
        EmployeeFile.objects.create(employee_file = emp_file)
        fname = EmployeeFile.objects.all().latest("id").employee_file
        filepath = os.path.join(path,'media/'+str(fname))
        xls = pd.ExcelFile(filepath)
        namelist = xls.sheet_names
        print(namelist)
        try:
            for sheetname in namelist:
                # ------------------ CO_ORDINATORS --------------------------
                if sheetname  ==  'CO-ORDINATORS':
                    print('CO-ORDINATORS')
                    crdntors = pd.read_excel(filepath,sheet_name='CO-ORDINATORS')
                    if EmployeeList.objects.filter(designation='co-ordinators'):
                        # EmployeeList.objects.filter(designation='co-ordinators').delete()
                        for i,row in crdntors.iterrows():
                            ifid = row['IFID']
                            if EmployeeList.objects.filter(ifid=ifid).exists():
                                pass
                            else:
                                 EmployeeList.objects.create(ifid=row['IFID'],name=row['NAME'],designation='co-ordinators')
                    else:
                        for i,row in crdntors.iterrows():
                            print(row['IFID'],row['NAME'])
                            EmployeeList.objects.create(ifid=row['IFID'],name=row['NAME'],designation='co-ordinators')
                # ------------------ ANNOTATORS --------------------------
                if sheetname == 'ANNOTATORS' :
                    print('ANNOTATORS')
                    annotators = pd.read_excel(filepath,sheet_name='ANNOTATORS')
                    if EmployeeList.objects.filter(designation='annotators'):
                        # EmployeeList.objects.filter(designation='annotators').delete()
                        for i,row in annotators.iterrows():
                            ifid = row['IFID']
                            if  EmployeeList.objects.filter(ifid=ifid).exists():
                                pass 
                            else:
                                EmployeeList.objects.create(ifid=row['IFID'],name=row['NAME'],designation='annotators')
                    else:
                        for i,row in annotators.iterrows():
                            print(row['IFID'],row['NAME'])
                            EmployeeList.objects.create(ifid=row['IFID'],name=row['NAME'],designation='annotators')
                # ------------------ HR TEAM --------------------------
                if sheetname == 'HR TEAM':
                    print('HR TEAM')
                    annotators = pd.read_excel(filepath,sheet_name='HR TEAM')
                    if EmployeeList.objects.filter(designation='hrteam'):
                        # EmployeeList.objects.filter(designation='hrteam').delete()
                        for i,row in annotators.iterrows():
                            ifid = row['IFID']
                            if EmployeeList.objects.filter(ifid=ifid).exists():
                                pass
                            else:
                                EmployeeList.objects.create(ifid=row['IFID'],name=row['NAME'],designation='hrteam')
                    else:
                        for i,row in annotators.iterrows():
                            print(row['IFID'],row['NAME'])
                            EmployeeList.objects.create(ifid=row['IFID'],name=row['NAME'],designation='hrteam')
                # ------------------ TEHNICAL TEAM --------------------------
                if sheetname == 'TECH':
                    print('TECH')
                    technical = pd.read_excel(filepath,sheet_name='TECH')
                    if EmployeeList.objects.filter(designation='technical'):
                        # EmployeeList.objects.filter(designation='technical').delete()
                        for i,row in technical.iterrows():
                            ifid = row['IFID']
                            if not EmployeeList.objects.filter(ifid=ifid).exists():
                                EmployeeList.objects.create(ifid=row['IFID'],name=row['NAME'],designation='technical')
                    else:
                        for i,row in technical.iterrows():
                            print(row['IFID'],row['NAME'])
                            EmployeeList.objects.create(ifid=row['IFID'],name=row['NAME'],designation='technical')
                messages.success(request,'File uploaded succesfully!')
            
        except Exception as er:
            print(er)
            messages.error(request,er)
        return redirect ('hr-home')



@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin','hrteam'])
def export_EMPfile(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Employees.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('CO-ORDINATORS') # this will make a sheet named Users Data
    wa = wb.add_sheet('ANNOTATORS')
    wh = wb.add_sheet('HR TEAM')
     # Sheet header, first row
    row_num = 0
    row_num1 = 0
    row_num2 = 0
   
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['IFID','NAME' ]

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    ################# CO-ORDINATORS ################
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    rows = EmployeeList.objects.filter(designation='co-ordinators').values_list('ifid','name')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    ####################### ANNOTATORS #######################
    for col_num in range(len(columns)):
        wa.write(row_num1, col_num, columns[col_num], font_style) # at 0 row 0 column

    rowsa = EmployeeList.objects.filter(designation='annotators').values_list('ifid','name')
    for row in rowsa:
        row_num1 += 1
        for col_num in range(len(row)):
            wa.write(row_num1, col_num, row[col_num], font_style)

    ######################### HR TEAM ###############################
    for col_num in range(len(columns)):
        wh.write(row_num2, col_num, columns[col_num], font_style) # at 0 row 0 column

    rowsh = EmployeeList.objects.filter(designation='hrteam').values_list('ifid','name')
    for row in rowsh:
        row_num2 += 1
        for col_num in range(len(row)):
            wh.write(row_num2, col_num, row[col_num], font_style)

    wb.save(response)
    return response

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin','hrteam'])
def add_ANNOTATOR(request):
    if request.method == "POST":
        ifid = request.POST.get('ifid')
        name = request.POST.get('name')
        print(ifid , name)
        exist = EmployeeList.objects.filter(ifid=ifid ,designation='annotators')
        if not exist:
            EmployeeList.objects.create(ifid=ifid ,name=name ,designation='annotators')
            messages.success(request,f'Added {ifid} succesfully!')
        else:
            messages.error(request,f'IFID {ifid} already exists!')
    return redirect('hr-home')
@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin','hrteam'])
def add_TECHNICAL(request):
    if request.method == "POST":
        ifid = request.POST.get('ifid')
        name = request.POST.get('name')
        print(ifid , name)
        exist = EmployeeList.objects.filter(ifid=ifid ,designation='technical')
        if not exist:
            EmployeeList.objects.create(ifid=ifid ,name=name ,designation='technical')
            messages.success(request,f'Added {ifid} succesfully!')
        else:
            messages.error(request,f'IFID {ifid} already exists!')
    return redirect('hr-home')

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin','hrteam'])
def add_COORDINATOR(request):
    if request.method == "POST":
        ifid = request.POST.get('ifid')
        name = request.POST.get('name')
        print(ifid , name)
        exist = EmployeeList.objects.filter(ifid=ifid ,designation='co-ordinators')
        if not exist:
            EmployeeList.objects.create(ifid=ifid ,name=name ,designation='co-ordinators')
            messages.success(request,f'Added {ifid} succesfully!')
        else:
            messages.error(request,f'IFID {ifid} already exists!')
    return redirect('hr-home')

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin','hrteam'])
def add_HRteam(request):
    if request.method == "POST":
        ifid = request.POST.get('ifid')
        name = request.POST.get('name')
        print(ifid , name)
        exist = EmployeeList.objects.filter(ifid=ifid ,designation='hrteam')
        if not exist:
            EmployeeList.objects.create(ifid=ifid ,name=name ,designation='hrteam')
            messages.success(request,f'Added {ifid} succesfully!')
        else:
            messages.error(request,f'IFID {ifid} already exists!')
    return redirect('hr-home')

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin','hrteam'])
def edit_employee(request,pk):
    print(pk)
    if request.method == "POST":
        ifid = request.POST.get('ifid')
        name = request.POST.get('name')
        print(ifid , name)
        emp = EmployeeList.objects.get(id=pk)
        designation = EmployeeList.objects.get(id=pk).designation
        print(designation)
        if EmployeeList.objects.filter(ifid=ifid).exists():
            print('vhgbhb')
            emp.ifid = ifid
            emp.name = name
            emp.designation = designation
            emp.save()
            messages.success(request,f'Edited {ifid} succesfully!')
        else:
            messages.error(request,f'IFID {ifid} not exists!')
    return redirect('hr-home')
@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin','hrteam'])
def del_EMP(request,pk):
    EmployeeList.objects.get(id=pk).delete()
    messages.success(request,'data deleted succesfully!')
    return redirect('hr-home')


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin','hrteam'])
def conversion(request):
    if request.method == 'POST':
        final_data = [] # for output csv data; 
        fieldnames = ['SL NO', 'IFID', 'NAME']
        id_details = {}
        totaldays = 0
        xlfiles = request.FILES.getlist('Excelfiles')
        try:
            for file in xlfiles:
                read_sheet = pd.read_excel(file,sheet_name='Att.log report',skiprows=3)
                # Fill NaN Values ========>> 0
                read_sheet = read_sheet.fillna(0)
                column_names = read_sheet.columns
                datalist = []
                for i , row in read_sheet.iterrows():
                    datalist.append(row)
                dates = []
                nameindexkey = column_names[10]
                idindex = column_names[2]
                for d in column_names:
                    if str(d).isnumeric():
                        dates.append(str(d))
                        if str(d) not in fieldnames:
                            totaldays+=1
                            fieldnames.append(str(d))
                n = 2
                final_list = [datalist[i * n:(i + 1) * n] for i in range((len(datalist) + n - 1) // n )]
                for f in final_list:
                    if len(f)==2:
                        ifid = int(f[0][idindex])
                        name = f[0][nameindexkey]
                        # print(ifid, name)
                        if (ifid) in id_details:
                            date_time = id_details[ifid]['data']
                            ifname = id_details[ifid]['name']
                            # check name ==IFID
                            # if np.isnan(row[]):
                            if str(name).isnumeric() or name=='' :
                                name = ifname

                            for d in dates:
                                ptime = f[1][int(d)]
                                if ptime:
                                    if len(ptime)%5==0:
                                        ptime = textwrap.wrap(ptime,5)
                                    else:
                                        print('error .....',len(ptime))
                                else:
                                    ptime = []
                                if d in date_time:
                                    if ptime:
                                        date_time[d].extend(ptime)
                                        id_details[ifid]['data'][d] = date_time[d]
                                    
                                else:
                                    id_details[int(ifid)]['data'][d] = ptime
                                
                            id_details[ifid] = {'name':name, 'data':date_time}
                        else:          
                            date_time = {}
                            for d in dates:
                                ptime = f[1][int(d)]
                                if ptime:
                                    if len(ptime)%5==0:
                                        ptime = textwrap.wrap(ptime,5)
                                        # print(ptime)
                                    else:
                                        print('error .....',len(ptime))
                                else:
                                    ptime = []
                                date_time[d] = ptime
                                
                            # print(ifid,date_time)        
                            id_details[ifid] = {'name':name, 'data':date_time}
        
        
            for id in sorted(id_details):
                idDict = {}
                dtimedata = id_details[id]['data']
                attndcecount = 0

                idDict['IFID'] = id
                idDict['NAME'] = id_details[id]['name']
                # print( id,id_details[id]['name'])
                print(f'merging ...... IF {id}')
                for d in dtimedata:
                    if dtimedata[d]:
                        idDict[d] ='\n'.join(dtimedata[d])
                        attndcecount+=1
            
                final_data.append(idDict)
            # print(final_data)

            coordinators = EmployeeList.objects.filter(designation='co-ordinators')
            annotators = EmployeeList.objects.filter(designation='annotators')
            hrteam = EmployeeList.objects.filter(designation='hrteam')
            # --------------------------- CO_ORDINATORS -----------------------------
            crd_data = []
            slno = 0
            for crd in coordinators:
                crd_id = crd.ifid
                crd_name = crd.name
                for row in final_data[1:]:
                    ifid = int(row['IFID'])
                    if ifid == crd_id:
                        row_copy = row.copy()
                        slno+=1
                        print(f'sorting coordinator........ IF {ifid} , {slno}')
                        row_copy['SL NO'] = slno
                        row_copy['NAME'] = crd_name
                        crd_data.append(row_copy) 
            # print(crd_data)
            # ----------------------------- ANNOTATORS -----------------------------
            ann_data = []
            slno = 0
            for ann in annotators:
                ann_id = ann.ifid
                ann_name = ann.name
                for row in final_data[1:]:
                    ifid = int(row['IFID'])
                    if ifid == ann_id:
                        slno+=1
                        print(f'sorting annotator........ IF {ifid} , {slno}')
                        row['SL NO'] = slno
                        row['NAME'] = ann_name
                        ann_data.append(row)
            # print(crd_data)
            # ----------------------------- HR TEAM -----------------------------
            HR_data = []
            slno = 0
            for hr in hrteam:
                hr_id = hr.ifid
                hr_name = hr.name
                for row in final_data[1:]:
                    ifid = int(row['IFID'])
                    if ifid == hr_id:
                        slno+=1
                        print(f'sorting HR........ IF {ifid} , {slno}')
                        row['SL NO'] = slno
                        row['NAME'] = hr_name
                        HR_data.append(row)
            # print(crd_data)
            # -------------------- DOWNLOAD SORTED FILES -----------------------
            date = datetime.today().strftime('%d-%m-%Y')
            csv_files = {'coordinators':crd_data ,'annotators':ann_data,'hrteam':HR_data}
            zipped_file = BytesIO()
            with zipfile.ZipFile(zipped_file, 'a', zipfile.ZIP_DEFLATED) as zipped:
                for data in csv_files:  # determines which csv file to write
                    csv_data = StringIO()
                    writer = csv.DictWriter(csv_data,fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(csv_files[data])
                    csv_data.seek(0)
                    zipped.writestr(f"{data}_{date}.csv", csv_data.read())
            zipped_file.seek(0)
            response = HttpResponse(zipped_file, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename=sorted_punching_{date}.zip'
            return response
            
        except Exception as er:
            messages.error(request,er)


    return redirect('hr-home')

