from django.shortcuts import redirect, render

from accounts.decorators import allowed_users
from .models import IFMessages,msgFiles
from django.utils import timezone
from django.contrib import messages
import os
from django.views.decorators.csrf import csrf_exempt 
from .forms import IFmessageForm
from accounts.models import EmployeeDetails
from django.contrib.auth.decorators import login_required


def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return days,hours, minutes, seconds


# Create your views here.
@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def messageHome(request):
    ifomessages = IFMessages.objects.all().order_by('id').reverse()

    for im in ifomessages:
        # fname = str(im.file).split('messages/files/')[-1]
        # im.filename = fname
        msgfiles = msgFiles.objects.filter(message=im)
        for i in msgfiles:
            fname = str(i.files).split('messages/files/')[-1]
            ext = os.path.splitext(fname)[-1]
            i.fname = fname
            i.ext = ext
        im.msgfiles = msgfiles
        if im.updated_at:
            timelaps = timezone.now() - im.updated_at
            days, hours, minutes, seconds = convert_timedelta(timelaps)
            if days:
                if days==1:
                    im.timelaps = str(days)+' day'
                elif days>=31:
                    im.timelaps = str(days//30)+' month'
                else:
                    im.timelaps = str(days)+' days'
            elif hours:
                im.timelaps = str(hours)+' hr'
            elif minutes:
                im.timelaps = str(minutes)+' min'
            else:
                im.timelaps = str(seconds)+' sec'
     
    context = {'page_title':'INFOLKS | Messages' , 'ifmessages':ifomessages}
    return render(request,'home.html',context)


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def addMessage(request):
    title = request.POST.get('title')
    descrptn = request.POST.get('description')
    files = request.FILES.getlist('msg-files')
    # print(files)
    # print(updatedat)
    messsage = IFMessages.objects.create(title=title , description=descrptn)
    for file in files:
        msgFiles.objects.create(message=messsage, files=file)
    EmployeeDetails.objects.all().update(unread_msg=True)
    messages.success(request,f"message: {title}  added successfully!")
    
    return redirect('messagehome')


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def deleteMessage(request,pk):
    del_msg = IFMessages.objects.get(id=pk)
    messages.success(request,f"message: {del_msg.title}  deleted!")
    print(del_msg.title)
    del_msg.delete()
    return redirect('messagehome')


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def editMessage(request,pk):
    # print('edit function...')
    edit_msg = IFMessages.objects.get(id=pk)
    form = IFmessageForm(instance=edit_msg)
    if request.method =='POST':
        form = IFmessageForm(request.POST, instance=edit_msg)
        if form.is_valid():
            form.save()
            update_date = timezone.now()
            edit_msg.updated_at = update_date
            edit_msg.save()

            messages.success(request,f'{edit_msg.title}  updated succesfully!')
            return redirect('messagehome')
        else:
            messages.error(request,form.errors)
        
    context = {'page_title':'INFOLKS | Messages' ,'editmsg':edit_msg, 'form':form}
    return render(request,'editmsg.html',context)

@csrf_exempt
@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def file_upload_save(request):
    title = request.POST.get('title')
    descrptn = request.POST.get('description')
    files = request.FILES.getlist('file')
    messsage = IFMessages.objects.create(title=title , description=descrptn)
    for file in files:
        print(file)
        msgFiles.objects.create(message=messsage, files=file)
    EmployeeDetails.objects.all().update(unread_msg=True)
    messages.success(request,f"message: {title}  added successfully!")

    return redirect('messagehome')

# ======================  USER VIEW ========================
@login_required(login_url='loginpage')
def id_notifications(request):
    empname = request.user
    ifid = EmployeeDetails.objects.get(empname=empname).if_id
    msg_data = EmployeeDetails.objects.filter(empname=empname)
    msg_data.update(unread_msg=False)
    unreadmsg = EmployeeDetails.objects.get(empname=empname).unread_msg
    ifomessages = IFMessages.objects.all().order_by('id').reverse()
    for im in ifomessages:
        msgfiles = msgFiles.objects.filter(message=im)
        for i in msgfiles:
            fname = str(i.files).split('messages/files/')[-1]
            ext = os.path.splitext(fname)[-1]
            i.fname = fname
            i.ext = ext
        im.msgfiles = msgfiles
        if len(str(im.description))>200:
            im.readless ,im.readmore= str(im.description)[:220] , str(im.description)[220:]
        im.last_updated = im.upload_date
        if im.updated_at:
            im.last_updated = im.updated_at
            timelaps = timezone.now() - im.updated_at
            days, hours, minutes, seconds = convert_timedelta(timelaps)

            if days:
                if days==1:
                    im.timelaps = str(days)+' day'
                elif days>=31:
                    im.timelaps = str(days//30)+' month'
                else:
                    im.timelaps = str(days)+' days'
            elif hours:
                im.timelaps = str(hours)+' hr'
            elif minutes:
                im.timelaps = str(minutes)+' min'
            else:
                im.timelaps = str(seconds)+' sec'

    return render(request,'user/msg_home.html',{'ifid':ifid,'empname':empname,'messages':ifomessages,'unreadmsg':unreadmsg,'page_title':'INFOLKS | Messages','nbar' : 'msgHome'})


@login_required(login_url='loginpage')
def msgReadmore(request,title):
    empname = request.user
    ifid = EmployeeDetails.objects.get(empname=empname).if_id
    msg_obj = IFMessages.objects.get(title=title)
    msgfiles = msgFiles.objects.filter(message=msg_obj)
    for i in msgfiles:
        fname = str(i.files).split('messages/files/')[-1]
        ext = os.path.splitext(fname)[-1]
        i.fname = fname
        print(fname)
        i.ext = ext
    msg_obj.msgfiles = msgfiles
    return render(request,'user/readmore.html',{'ifid':ifid,'empname':empname,'msg':msg_obj,'page_title':'INFOLKS | Messages','nbar' : 'msgHome'})