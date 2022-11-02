from email import message
from django.shortcuts import render  ,redirect

from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q

from .decorators import allowed_users, unauthenticated_user
from ifoadmin.models import EmployeeMobile
from .models import *
from .forms import *

def registeruser(request):
    form = SignUpForm()
    if request.method =='POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            userid = form.cleaned_data.get('empid')
            useremail = form.cleaned_data.get('email')
            phno = form.cleaned_data.get('mobileNo')
            pswd = form.cleaned_data.get('password1')
            print('signup form.... ',userid,username)
            usridexist = EmployeeDetails.objects.filter(if_id= userid).exists()
            mailexist = EmployeeDetails.objects.filter(emailid= useremail).exists()
            phnoexist = EmployeeDetails.objects.filter(mobileNo=phno ).exists()
            phnereg = EmployeeMobile.objects.filter(ifid=userid).exists()
            phnemtch = False
            if EmployeeMobile.objects.filter(ifid=userid).exists():
                if (EmployeeMobile.objects.filter(ifid=userid).first().mobile)==str(phno) :
                    phnemtch = True
                else:
                    phnemtch = False
            else:
                phnereg = False
            if not usridexist and not mailexist and not phnoexist and phnemtch and phnereg:
                user = form.save()
                print('signup successful :',userid,username,pswd)
                EmployeeDetails.objects.create(if_id = userid, empname = username,
                                            emailid = useremail, mobileNo = phno ,password = pswd)
                # validate otp
                # emotp = str(random.randint(10000 , 99999))
                # send_emailotp(useremail , emotp)
                # messages.success(request,'A message with verification code has been sent to your Email.')
                # return redirect('loginpage')
                group = Group.objects.get(name='employee')
                user.groups.add(group)
                messages.success(request,'Account was created for '+username)
                return redirect('loginpage')
            else:
                if not phnereg:
                    messages.error(request,'IFID-MobNo not added. Plz contact Admin!')
                elif usridexist:
                    messages.error(request,str(userid)+'  already exists!!')
                elif mailexist:
                    messages.error(request,'Mail ID  already exists!!')
                elif phnoexist:
                    messages.error(request,'Mobile Number Exists !!')
                elif not phnemtch:
                    messages.error(request,'Mobile Number doesn\'t match with registered number!!')

                return redirect('signuppage')
        else:
            def check(sentence, words):
                # res = [all([k in s for k in words]) for s in sentence]
                # return [sentence[i] for i in range(0, len(res)) if res[i]]
                flag = False
                for error in sentence:
                    if words in error:
                        flag=True
                return flag
            sentence = [v.__str__() for k, v in form.errors.items()]
            print(sentence)
            if check(sentence,'Enter a valid username'):
                msg = msg = "Username doesn't allow white space"
                messages.error(request,msg)
            elif check(sentence,'Enter a valid email address'):
                msg = msg = "Enter a valid email address"
                messages.error(request,msg)
            elif check(sentence,'The two password fields didn’t match'):
                msg = "The two password fields didn't match"
                messages.error(request,msg)
            elif check(sentence,'A user with that username already exists'):
                msg = "Username already exists"
                messages.error(request,msg)
            elif check(sentence,'This password is too short'):
                msg = "Password is too short"
                messages.error(request,msg)
            else:
                messages.error(request,sentence)          
            context={'form':form}
            return render(request,'register.html',context)
    context={'form':form}
    return render(request,'register.html',context)

def is_admin(user):
    return user.groups.filter(name='admin').exists()

def is_hr(user):
    return user.groups.filter(name='hrteam').exists()

@csrf_exempt
@unauthenticated_user
def loginPage(request):
    if request.method=='POST':
        inp = request.POST.get('mobno')
        if len(str(inp)) ==10 and inp.isnumeric():
            if EmployeeDetails.objects.filter(mobileNo= inp):
                empname = EmployeeDetails.objects.filter(mobileNo= inp).first().empname
            else:
                empname = inp
        else:
            empname = inp
        passwrd = request.POST.get('password')
        user = authenticate(request,username=empname ,password =passwrd)
        
        if user is not None:
            login(request,user)
            print(user)
            if is_admin(user):
                print('admin')
                return redirect('home')
            elif is_hr(user):
                print('hrteam')
                return redirect('hr-home')
            else:
                ifid = EmployeeDetails.objects.get(empname=empname).if_id
                oldpasswrd = EmployeeDetails.objects.get(empname=empname).password
                if passwrd!=oldpasswrd:
                    updateobj = EmployeeDetails.objects.get(empname=empname)
                    updateobj.password = passwrd
                    updateobj.save()
                print('employee:',empname,ifid )
                return redirect('attendance/home')
        else:
            messages.info(request,'Invalid credentials')
    context = {}
    return render(request,'index.html',context)


@login_required(login_url='loginpage')
def logoutUser(request):
    logout(request)
    return redirect('loginpage')


@csrf_exempt
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            print('password reset request:',data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
					"email":user.email,
					'domain':'attendance.infolksgroup.com:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'techinfolks16@gmail.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    
                    messages.success(request,'A message with reset password instructions has been sent to your inbox.')
                    return redirect('loginpage')

            else:
                messages.error(request,'Enter valid Email address!!')
                print('user not exist')
    password_reset_form = PasswordResetForm()     
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

# ----------------- ERRORS ---------------------------------

def error_404_page(request, exception):
    return render(request, 'errors/404.html', status=404)


def error_500_page(request):
    return render(request,'errors/500.html',status=500)
    
def error_403_page(request, exception):
    return render(request, 'errors/403.html', {})


def maintenance(request):
    return render(request, 'errors/maintenance.html')
