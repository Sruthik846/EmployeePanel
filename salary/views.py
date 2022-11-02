from django.shortcuts import render,redirect
from accounts.decorators import allowed_users
from django.contrib.auth.decorators import login_required
import time, datetime, os
from .models import *
from django.contrib import messages
import pandas as pd
import numpy as np
from .forms import *
from accounts.models import EmployeeDetails
from message.models import IFMessages
from django.http import HttpResponse

cpath = os.getcwd()

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def addsalaryMonth(request):
    ym = time.strftime("%Y-%m") 
    if request.method == 'POST':
        month_num = str(request.POST.get('yr-mnth').split("-")[-1])
        datetime_object = datetime.datetime.strptime(month_num, "%m")
        month = datetime_object.strftime("%B")
        yr  = str(request.POST.get('yr-mnth').split("-")[0])
        print(month,yr)
        if salaryMonth.objects.filter(year=yr,month=month).exists():
            messages.error(request,'data exists')
        else:
            salaryMonth.objects.create(year = yr,
                                    month= month)

    monthdatas = salaryMonth.objects.all().order_by('id').reverse()
    
    context = {'monthdata':monthdatas,'page_title':'MonthWise Details','ym':ym}
    return render(request,'salaryhome.html',context)

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def viewSalaryFiles(request,year,month):
    salary_files = SalaryFile.objects.filter(month=month,year=year)
    for sl in salary_files:
        fname = str(sl.file).split('/')[-1]
        sl.file = fname
    navitems = {'Monthwise':'salaryhome'}
    context = {'salaryfile':salary_files,'page_title':'Salary files','year':year,'month':month,'navitems':navitems}
    return render(request,'salary_files.html',context)

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def idSalaryDetails(request,year,month):
    salary_details = SalaryDetails.objects.filter(year=year,month=month).order_by('ifid')
    for ids in salary_details:
        if GrandTotal.objects.filter(basicSalary=ids).exists():
            grandtotal_obj = GrandTotal.objects.get(basicSalary=ids)
            grandtotal = grandtotal_obj.total
            ids.grandtotal = grandtotal
            # print(ids.ifid,grandtotal)
    navitems = {'Monthwise':'salaryhome'}
    context = {'salarydetails':salary_details,'year':year,'month':month,'page_title':month+" | "+str(year),'navitems':navitems}
    return render(request,'table.html',context)

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def delSalary(request,month,year):
    slrymnth = salaryMonth.objects.get(month=month,year=year)
    slry_file = SalaryFile.objects.filter(month=month,year=year)
    mnth = month
    yr = year
    if slry_file:
        for sl in slry_file:
            fname = sl.file
            try:
                os.remove(os.path.join(cpath,'media/'+str(fname)))
            except Exception as er:
                print('delete error:',er)
    slry_file.delete()
    slrymnth.delete()
    SalaryDetails.objects.filter(month=mnth,year=yr).delete()
    messages.success(request,'data deleted succesfully!')
    return redirect('salaryhome')

# @login_required(login_url='loginpage')
# @allowed_users(allowed_roles=['admin'])
# def uploadSalaryFile(request,month,year):
#     if request.method == 'POST':
#         SalaryFile.objects.create(file = request.FILES.get('salaryfile'),
#                                 year = year,
#                                 month= month, status='PENDING')
#         salary_files = SalaryFile.objects.filter(month=month,year=year)
#         latest_id = None
#         if salary_files:
#             latest_id = SalaryFile.objects.latest('id').id
#         for sl in salary_files:
#             fname = str(sl.file).split('/')[-1]
#             sl.file = fname
#         navitems = {'Monthwise':'salaryhome'}
#         context = {'salaryfile':salary_files,'page_title':'Salary files','year':year,'month':month,'navitems':navitems,'latest_id':latest_id}
#         return render(request,'salary_file_upload.html',context)

# @login_required(login_url='loginpage')
# @allowed_users(allowed_roles=['admin'])
# def uploadSalaryData(request,month,year):
#     fname = SalaryFile.objects.latest('id').file
#     f_id = SalaryFile.objects.latest('id').id
#     filepath = os.path.join(cpath,'media/'+str(fname))
#     print(filepath)
#     data_values = {'filepath' : filepath, 'month' : month, 'year' : year,'file_id':f_id}
#     task = salary_upload.delay(data_values)

#     latest_id = None
#     salary_files = SalaryFile.objects.filter(month=month,year=year)
#     for sl in salary_files:
#             fname = str(sl.file).split('/')[-1]
#             sl.file = fname
#     navitems = {'Monthwise':'salaryhome'}
#     context = {'salaryfile':salary_files,'page_title':'Salary files','year':year,'month':month,'navitems':navitems,'latest_id':latest_id,'task_id' : task.task_id}
#     return render(request,'salary_file_upload.html',context)
    

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def uploadSalaryFile2(request,month,year):
    if request.method == 'POST':
        SalaryFile.objects.create(file = request.FILES.get('salaryfile'),
                                year = year,
                                month= month)
    ###########-------- ADD DETAILS TO DATABASE ---------###########
        fname = SalaryFile.objects.latest('id').file
        filepath = os.path.join(cpath,'media/'+str(fname))
        print(pd.ExcelFile(filepath).sheet_names)
        try:
            xls = pd.read_excel(filepath,skiprows=1,sheet_name='salary details',)
            column_names = xls.columns
            for i,row in xls.iterrows():
                # print(row)
                ifname = row['Name']
                ifid = row['IFID']
                if not np.isnan( ifid) :
                    for x in column_names:
                        if row[x]==' ':
                            row[x]=0
                    row.fillna(value=0,inplace=True)
                    dataexist = SalaryDetails.objects.filter(ifid = ifid,month = month,year = year)

                    if not dataexist:
                        print(ifid,ifname)

                        #  Basic Salary Details ----------------
                        SalaryDetails.objects.create(ifid=ifid, name=ifname, month=month, year=year,
                                                    grade=row['Grade'], attendance=row['Attendance'], salary=row['Grade Salary'],
                                                    training_att = 0, training_salary=row['Training'],
                                                    bonus = row['Bonus'], night_shift = row['Night Shift'], rent=row['Rent'],
                                                    other=row['Other'], total_salary =int( row['Work Salary']), total_other_income = row['Total Other Income']
                                                    )
                        idSalaryObj = SalaryDetails.objects.get(ifid = ifid,month = month,year = year)

                        # Special Income -----------
                        if not specialIncome.objects.filter(basicSalary=idSalaryObj).exists():
                            specialIncome.objects.create(basicSalary=idSalaryObj, HRA=row['HRA'], invest_profit=row['Investment Profit'],
                                                    Rsg_settlement=row['Rsg. Settlement'], minimum_wage=row['Minimum Wage'], 
                                                    survey_scheme=row['Thanal'] ,from_last_month=row['From Last Month'], 
                                                    festival_bonus=row['Festival Bonus'], savings=row['Savings'], total=row['Special Total'])

                        # Deductions ---------------
                        if not Deductions.objects.filter(basicSalary=idSalaryObj).exists():
                            Deductions.objects.create(basicSalary=idSalaryObj, to_next_month=row['To Next Month'],
                                                other=row['Deduction Other'], total=row['Deduction Total'])

                        # Grand Total ---------------
                        if not GrandTotal.objects.filter(basicSalary=idSalaryObj).exists():
                            GrandTotal.objects.create(basicSalary=idSalaryObj , total=row['Grand Total'])
                    else:
                        print(ifid,ifname,'  already exists...')
        
        except Exception as er:
            fname = SalaryFile.objects.latest('id').file
            SalaryFile.objects.filter(month=month,year=year).delete()
            filepath = os.path.join(cpath,'media/'+str(fname))
            if os.path.exists(filepath):
                os.remove(filepath)
            SalaryDetails.objects.filter(month=month,year=year).delete()
            messages.error(request,f"Error  : \n{er} Plz validate file and upload again!!")
            return redirect('salaryhome')

        messages.success(request,'File uploaded successfully.')
    return redirect('salaryhome')


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def add_id_salary(request,year,month):
    if request.method == "POST":
        ifid = request.POST.get("ifid")
        name = request.POST.get("name")
        if SalaryDetails.objects.filter(ifid=ifid,month=month,year=year).exists():
            print('salary for',ifid,'exists')
            messages.error(request,f'salary details for IFID: {ifid} already exists!')

        else:
            # Basic salary --------------------------------
            grade = request.POST.get("grade")
            attendance = request.POST.get("attendance")
            grade_salary = request.POST.get("grade_salary")
            training = request.POST.get("training")
            bonus = request.POST.get("bonus")
            night_shift = request.POST.get("night_shift")
            rent = request.POST.get("rent")
            basic_other = request.POST.get("basic_other")
            basic_other_total = request.POST.get("basic_other_total")
            basic_total = request.POST.get("basic_total")

            SalaryDetails.objects.create(ifid=ifid,name=name, month=month,year=year, grade=grade, 
                                        attendance=attendance, salary=grade_salary, training_salary=training, 
                                        bonus=bonus, night_shift=night_shift,rent=rent , 
                                        other=basic_other , total_salary=basic_total,total_other_income=basic_other_total
                                        )
            BasicSalary = SalaryDetails.objects.get(ifid=ifid, month=month,year=year)
            # special Income ------------------------------------
            hra = request.POST.get("hra")
            invest_profit = request.POST.get("invest_profit")
            rsg_settle = request.POST.get("rsg_settle")
            minimum_wage = request.POST.get("minimum_wage")
            from_last_month = request.POST.get("from_last_month")
            festival_bonus = request.POST.get("festival_bonus")
            savings = request.POST.get("savings")
            special_total = request.POST.get("special_total")
            thanal = request.POST.get("thanal")

            specialIncome.objects.create(basicSalary=BasicSalary, HRA=hra, invest_profit=invest_profit,
                                        Rsg_settlement=rsg_settle, minimum_wage=minimum_wage, from_last_month=from_last_month,
                                        festival_bonus=festival_bonus, savings=savings, total=special_total,survey_scheme=thanal
                                        )
            # deductions
            to_next_month = request.POST.get("to_next_month")
            deduction_other = request.POST.get("deduction_other")
            deduction_total = request.POST.get("deduction_total")

            Deductions.objects.create(basicSalary=BasicSalary, to_next_month=to_next_month, 
                                    other=deduction_other, total=deduction_total
                                    )
            # grand Total
            grand_total = request.POST.get("grand_total")
            GrandTotal.objects.create(basicSalary=BasicSalary , total=grand_total)
            
            print('added salary details for',ifid,name)
            messages.success(request,f'added salary details for {ifid}')
    
    return redirect(f'/salary/{year}/{month}')


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def idSalary(request,year,month,ifid):
    basic_salary = SalaryDetails.objects.get(year=year,month=month,ifid=ifid)
    special_incomes = specialIncome.objects.filter(basicSalary=basic_salary)
    deductions = Deductions.objects.filter(basicSalary=basic_salary)
    grand_total = GrandTotal.objects.filter(basicSalary=basic_salary)

    
    if special_incomes.exists():
        special_income = specialIncome.objects.get(basicSalary=basic_salary)
        special_income_form = specialIncomeForm(instance=special_income)
    else:
        special_income=[]
        special_income_form = []
    if deductions.exists():
        deduction = Deductions.objects.get(basicSalary=basic_salary)
        deduction_form = deductionForm(instance=deduction)
    else:
        deduction = []
        deduction_form = []
    if grand_total.exists():
        grandtotal = GrandTotal.objects.get(basicSalary=basic_salary)
        grndtotal = GrandTotal.objects.get(basicSalary=basic_salary).total
        GR_Total_form = GR_Total_Form(instance=grandtotal)
    else:
        grndtotal = []
        GR_Total_form = Basic_Total_Form(instance=basic_salary)


    # FOR UPDATION --------------------------------------
    basic_salary_form = salaryform(instance=basic_salary)
    

    context = {'basic_salary':basic_salary,'special_income':special_income ,'deductions':deduction,'grand_total':grndtotal,
                'basic_salary_form':basic_salary_form,'special_income_form':special_income_form,
                'deduction_form':deduction_form,'GR_Total_form':GR_Total_form
            }
    return render(request,'id_salary.html',context)


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def del_id_salary(request,year,month,ifid):
    basic_object = SalaryDetails.objects.get(year=year,month=month,ifid=ifid)
    basic_object.delete()
    messages.success(request,'data deleted succesfully!')
    print(f'salary of ifid: {ifid} deleted!')
    return redirect(f'/salary/{year}/{month}')


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def editBasicSalary(request,year,month,ifid):
    update_object = SalaryDetails.objects.get(year=year,month=month,ifid=ifid)
    form = salaryform(instance=update_object)
    if request.method =='POST':
        form = salaryform(request.POST, instance=update_object)
        if form.is_valid():
            print('valid')
            form.save()
            messages.success(request,'data updated succesfully!')
            return redirect(f'/salary/{year}/{month}/{ifid}/view')
        else:
            print('invalid')
            messages.error(request,form.errors)
            return redirect(f'/salary/{year}/{month}/{ifid}/view')
    context = {'form':form,'month':month,'year':year}
    return redirect(f'/salary/{year}/{month}/{ifid}/view')


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def editSpecialIncome(request,year,month,ifid):
    basic_object = SalaryDetails.objects.get(year=year,month=month,ifid=ifid)
    update_object = specialIncome.objects.get(basicSalary=basic_object)
    form = specialIncomeForm(instance=update_object)
    if request.method =='POST':
        form = specialIncomeForm(request.POST, instance=update_object)
        if form.is_valid():
            print('valid')
            form.save()
            messages.success(request,'data updated succesfully!')
            return redirect(f'/salary/{year}/{month}/{ifid}/view')
        else:
            print('invalid')
            print(form.errors)
            messages.error(request,form.errors)
    return redirect(f'/salary/{year}/{month}/{ifid}/view')


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def editDeductions(request,year,month,ifid):
    basic_object = SalaryDetails.objects.get(year=year,month=month,ifid=ifid)
    update_object = Deductions.objects.get(basicSalary=basic_object)
    form = deductionForm(instance=update_object)
    if request.method =='POST':
        form = deductionForm(request.POST, instance=update_object)
        if form.is_valid():
            print('valid')
            form.save()
            messages.success(request,'data updated succesfully!')
            return redirect(f'/salary/{year}/{month}/{ifid}/view')
        else:
            print('invalid')
            print(form.errors)
            messages.error(request,form.errors)
    return redirect(f'/salary/{year}/{month}/{ifid}/view')


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def editGrandTotal(request,year,month,ifid):
    basic_object = SalaryDetails.objects.get(year=year,month=month,ifid=ifid)
    other_exist = False
    if  GrandTotal.objects.filter(basicSalary=basic_object).exists():
        update_object = GrandTotal.objects.get(basicSalary=basic_object)
        form = GR_Total_Form(instance=update_object)
        other_exist = True
    else:
        form = Basic_Total_Form(instance=basic_object)

    if request.method =='POST':
        if other_exist:
            form = GR_Total_Form(request.POST, instance=update_object)
        else:
            form = Basic_Total_Form(request.POST,instance=basic_object)
        if form.is_valid():
            print('valid')
            form.save()
            messages.success(request,'data updated succesfully!')
            return redirect(f'/salary/{year}/{month}/{ifid}/view')
        else:
            print('invalid')
            print(form.errors)
            messages.error(request,form.errors)
    return redirect(f'/salary/{year}/{month}/{ifid}/view')


#---------------------EMPLOYEE LOGIN-------------------------------
@login_required(login_url='loginpage')
def id_salaryhome(request):
    empname = request.user
    ifid = EmployeeDetails.objects.get(empname=empname).if_id
    if IFMessages.objects.all():
        unreadmsg = EmployeeDetails.objects.get(empname=empname).unread_msg
    else:
        unreadmsg = False
    dataexist = False
    salarymonths = SalaryFile.objects.all().order_by('id').reverse()
    mnthdata = []
    for sl in salarymonths:
        mnth = sl.month
        yr = sl.year
        id_salary = SalaryDetails.objects.filter(ifid =ifid ,year=yr,month=mnth)
        if id_salary:
            # print(id_details)
            id_salary = SalaryDetails.objects.get(ifid =ifid ,year=yr,month=mnth)
            dataexist = True
            if GrandTotal.objects.filter(basicSalary=id_salary).exists():
                grandtotal_obj = GrandTotal.objects.get(basicSalary=id_salary)
                grandtotal = grandtotal_obj.total
                id_salary.grandtotal = grandtotal
            if id_salary not in mnthdata:
                mnthdata.append(id_salary)
            # print(len(mnthdata))
    monthlatest = SalaryFile.objects.all().latest('id')
    mnlatestdata = []
    mon = monthlatest.month
    year = monthlatest.year
    if  SalaryDetails.objects.filter(ifid =ifid ,year=year,month=mon).exists():
        basic_salary = SalaryDetails.objects.get(ifid=ifid,month=mon,year=year)
        empname = EmployeeDetails.objects.get(if_id = ifid).empname
        special_incomes = specialIncome.objects.filter(basicSalary=basic_salary)
        deductions = Deductions.objects.filter(basicSalary=basic_salary)
        grand_total = GrandTotal.objects.filter(basicSalary=basic_salary)
        if special_incomes.exists():
            special_income = specialIncome.objects.get(basicSalary=basic_salary)
        else:
            special_income=[]
        if deductions:
            deduction = Deductions.objects.get(basicSalary=basic_salary)
        else:
            deduction = []
        if grand_total.exists():
            grndtotal = GrandTotal.objects.get(basicSalary=basic_salary).total
        else:
            grndtotal = []
    if dataexist:
        # print(mnthdata)
        return render(request,'user/salary_home.html',{'ifid':ifid,'empname':empname,'monthdata':mnthdata,'page_title':'INFOLKS | Salary','unreadmsg':unreadmsg, 'nbar' : 'idsalary','monthlatest':mnlatestdata,
        'salarydata':basic_salary,'special_income':special_income ,
            'deductions':deduction,'grand_total':grndtotal,
            'page_title': 'INFOLKS | Salary',
            'month':mon,'year':year,'ifid':ifid,'empname':empname,'nbar' : 'idsalary'})
    else:
        # messages.error(request,'No details available')
        return render(request,'user/salary_home.html',{'ifid':ifid,'empname':empname,'page_title':'INFOLKS | Salary','unreadmsg':unreadmsg,'nbar' : 'idsalary'})

@login_required(login_url='loginpage')
def id_salaryData(request,year,month):
    empname = request.user
    ifid = EmployeeDetails.objects.get(empname=empname).if_id
    basic_salary = SalaryDetails.objects.get(ifid=ifid,month=month,year=year)
    empname = EmployeeDetails.objects.get(if_id = ifid).empname
    special_incomes = specialIncome.objects.filter(basicSalary=basic_salary)
    deductions = Deductions.objects.filter(basicSalary=basic_salary)
    grand_total = GrandTotal.objects.filter(basicSalary=basic_salary)

    if special_incomes.exists():
        special_income = specialIncome.objects.get(basicSalary=basic_salary)
    else:
        special_income=[]
    if deductions:
        deduction = Deductions.objects.get(basicSalary=basic_salary)
    else:
        deduction = []
    if grand_total.exists():
        grndtotal = GrandTotal.objects.get(basicSalary=basic_salary).total
    else:
        grndtotal = []
    
    context = {'salarydata':basic_salary,'special_income':special_income ,
            'deductions':deduction,'grand_total':grndtotal,
            'page_title': 'INFOLKS | Salary',
            'month':month,'year':year,'ifid':ifid,'empname':empname,'nbar' : 'idsalary'}
    return render (request,'user/salary_detailed.html',context)