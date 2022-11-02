from django.shortcuts import render,redirect
from accounts.models import EmployeeDetails
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_users, unauthenticated_user
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import *
from .models import *
import os,shutil
import pandas as pd


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def home(request):
    return render(request,'homepage.html',{'page_title':'Home'})

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def userpage(request):
    usercount = EmployeeDetails.objects.all().count()
    print('total users:',usercount)
    return render(request,'dashboard_usr.html',{'usercount':usercount,'page_title':'User Details'})

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def viewUsers(request):
    users = EmployeeDetails.objects.all()
    context = {'userdata':users,'navitems':{'USERS':'userpage'}}
    return render(request,'users.html',context)

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
# users table
def delUser(request,pk):
    userdata = EmployeeDetails.objects.get(if_id=pk)
    username = userdata.empname
    # print(username)
    user = User.objects.get(username=username)
    userdata.delete()
    user.delete()
    messages.success(request,'user deactivation successful.')
    return redirect('users')

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def uploadcred(request):
    if request.method == 'POST':
        fname = request.FILES.get('credfile')
        print(fname)
        CredFile.objects.create(xlfile = fname)
        file = CredFile.objects.all().first()
        path = os.getcwd()
        filepath = os.path.join(path,'media/'+str(file.xlfile))
        print(filepath)
        xls = pd.read_excel(fname,sheet_name='Projects')
        print(xls)
        uploadcount = 0
        errorids = []
        exist_error = []
        for i,row in xls.iterrows():
            print(row)
            
            mobileno = str(row['Mobile number']).replace(" ","")
            mobileerror = False
            if len(str(mobileno))!=10:
                mobileerror = True
                errorids.append(row['IFID'])
            ifexist = EmployeeMobile.objects.filter(ifid = row['IFID']).exists()
            mobexist = EmployeeMobile.objects.filter(mobile = mobileno).exists()
            if not ifexist and not mobexist and not mobileerror:
                uploadcount+=1
                print(row['IFID'],row['NAME'],row['Mobile number'])
                EmployeeMobile.objects.create(ifid = row['IFID'],name=row['NAME'], mobile = mobileno)
            else:
                exist_error.append(row['IFID'])
        if uploadcount:
            messages.success(request,f"{uploadcount} datas uploaded successfully!")
        if errorids:
            messages.error(request,"Invalid mobile number for IFID s:"+str(errorids))
        if errorids:
            messages.error(request,"mobile number exists for IFID s:"+str(exist_error))

        CredFile.objects.all().delete()
        shutil.rmtree(os.path.join(path,'media/credfiles'))
    return redirect('usercred')

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def employeeCred(request):
    usercreds = EmployeeMobile.objects.all().order_by('ifid')
    form = credforms(request.POST)
    print(request.POST)
    if request.method == 'POST':
        print(request.FILES.get('credfile'))
        if form.is_valid():
            form.save()
            messages.success(request,'Data added succesfully!')
            return redirect('usercred')
        else:
            for field in form:
                for error in field.errors:
                    print(field,error)
            context = {'usercred':usercreds,'form':form ,}
            return render(request,'user_cred.html',context)
    
    query = request.GET.get('q')
    if query:
        # print(query)
        usercreds = EmployeeMobile.objects.all().order_by('ifid').filter(
            Q(ifid__icontains=query) | Q(name__icontains=query)
        ).distinct()
    
    paginator = Paginator(usercreds,1000)
    page = request.GET.get('page')
    try:
        rows = paginator.page(page)
    except PageNotAnInteger:
        rows = paginator.page(1)
    except EmptyPage:
        rows = paginator.page(paginator.num_pages)
    context = {'usercred':rows, 'navitems':{'USERS':'userpage'}, 'page_title':'User Credentials'}
    return render(request,'user_cred.html',context)

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def updateMobile(request,pk):
    print(pk)
    updcred = EmployeeMobile.objects.get(ifid=pk)
    form = updateCred(instance=updcred)
    print(updcred)
    if request.method =='POST':
        form = updateCred(request.POST, instance=updcred)
        if form.is_valid():
            if len(str(request.POST.get('mobile')))==10:
                form.save()
                messages.success(request,'Mobile Number updated succesfully!')
                return redirect('usercred')
            else:
                messages.error(request,'Mobile Number should be 10 digits')
        else:
            print('invalid')
            print(form.errors)
    context = {'form':form}
    return redirect('usercred')

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def deletecred(request,pk):
    usercred = EmployeeMobile.objects.get(ifid=pk)
    usercred.delete()
    return redirect('usercred')
