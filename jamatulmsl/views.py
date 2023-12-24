from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import metainformation
from .serializers import metainfoserializer
from rest_framework import status
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.renderers import TemplateHTMLRenderer
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template

# from django.template import loader
#  template = loader.get_template('template.html')


def index(request):

    return render(request, 'index.html')


def signupPage(request):

    if request.method == "POST":
        uname=request.POST.get("Username")
        fname=request.POST.get("Fname")
        lname=request.POST.get("Lname")
        email=request.POST.get("Emailid")
        pass1=request.POST.get("Password")
        pass2=request.POST.get("confirmPassword")

        if pass1 != pass2:
            messages.error(request, "Password doesn't match!")
            return redirect('signup')

        try:
            if User.objects.get(username = uname):
                messages.warning(request, "Username is already taken!")
                return redirect('signup')

        except Exception as identifier:
            pass

        try:
            if User.objects.get(email = email):
                messages.warning(request, "Email ID is already registered!")
                return redirect('signup')

        except Exception as identifier:
            pass

        myuser = User.objects.create_user(uname, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        messages.success(request, "SignUp Successful!")
        return render(request, 'login.html')

    return render(request, 'signup.html')

def loginPage(request):

    if request.method == "POST":
        uname=request.POST.get("Username")
        password=request.POST.get("Password")

        myuser = authenticate(username=uname, password=password)

        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login Successful!")
            return redirect('/')

        else:
            messages.error(request, "Invalid Credentials!")
            return redirect('/login')

    return render(request, 'login.html')


class savepersondetails(APIView):
    
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):

        idcount = metainformation.objects.all()
        idlst = []
        for i in  idcount.values_list():
            idlst.append(i[0])
        if len(idlst) == 0:
            latestindex = '1'
        else:
            latestindex = idlst[-1] + 1
        condata = {
            'ids' : str(latestindex),
        }
        print(condata)

        return render(request, 'registrationform.html', {'context': condata['ids'] })
    
    def post(self, request):

        serializer = metainfoserializer(data=request.data)
        if serializer.is_valid():


            if metainformation.objects.filter(Contact_number=request.data.get('Contact_number')).exists():
                return Response('Contact Number Already Exist')
            elif metainformation.objects.filter(Form_number=request.data.get('Form_number')).exists():
                return Response('Form Number Already Exist')


            metainformation.objects.get_or_create(
                                                USERID=request.user.username,
                                                Applicant_name=request.data.get('Applicant_name'),
                                                Deceased_name=request.data.get('Deceased_name'),
                                                Gender=request.data.get('Gender'),
                                                Contact_number=request.data.get('Contact_number'),
                                                Address=request.data.get('Address'),
                                                Deceased_address=request.data.get('Deceased_address'),
                                                Date=request.data.get('Date'),
                                                Date_of_death=request.data.get('Date_of_death'),
                                                time_of_death=request.data.get('time_of_death'),
                                                Cause_of_death=request.data.get('Cause_of_death'),
                                                Relationship=request.data.get('Relationship'),
                                                Form_number=request.data.get('Form_number'),
                                                Amount=request.data.get('Amount'))

            getdata = metainformation.objects.filter(Contact_number=request.data.get('Contact_number'))
            serialsdata = metainfoserializer(getdata, many=True)

            messages.success(request, "Your Applicant has been successfully added!")
            
            idcount = metainformation.objects.all()
            idlst = []
            for i in  idcount.values_list():
                idlst.append(i[0])
            latestindex = idlst[-1] + 1

            condata = {
                'ids' : str(latestindex),
            }
            
            return render(request, 'registrationform.html', {'context': condata['ids'] })
            # Hi Hello
            # return Response(template_name='registrationform.html')

            # return Response(data={'Data': serialsdata.data, 
            #                     'message': 'Details Saved Successfull', 
            #                     'status': status.HTTP_201_CREATED,}, template_name='registrationform.html')
        
        messages.success(request, "Invalid Entry")
        return Response(serializer.error_messages,status=400, template_name='registrationform.html')


def logoutPage(request):
    logout(request)
    messages.success(request, 'Logout Successful!')
    return redirect('index')





class listResume(APIView):

    def get(self, request):

        current_user = request.user.username
        userid = metainformation.USERID

        if metainformation.objects.filter(USERID = current_user).exists():
            profile=metainformation.objects.filter(USERID = current_user)
            return render(request, "listResume.html", {'profile':profile})
        return render(request, 'listResume.html', status=status.HTTP_200_OK)

    def post(self, request):
        current_user = request.user.username
        current_user = request.data.get('Contact_number')
        userid = metainformation.USERID

        if metainformation.objects.filter(userid = current_user).exists():
            profile=metainformation.objects.filter(userid = current_user)
            return render(request, "listResume.html", {'profile':profile})   
        return render(request, "listResume.html", status=status.HTTP_202_ACCEPTED)

# import io as BytesIO 
# from xhtml2pdf import pisa
# from django.template.loader import get_template
# from django.template import Context
# from django.http import HttpResponse
# from html import escape



# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     context = dict(context_dict)
#     html  = template.render(context)
#     result = BytesIO.BytesIO ()

#     pdf = pisa.pisaDocument(BytesIO .BytesIO (html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))



class viewResume(APIView):

    def post(self, request):
        try:
            contact = request.POST['Contact_number']
            user_profile = metainformation.objects.get(Contact_number=contact)
            template = get_template('burial.html')
            if  'button1' in request.POST:
                context ={
                     'user_profile':user_profile
                }
                html = template.render(context)
                # return render_to_pdf("burial.html", context)
                return render(request, "burial.html", {'user_profile':user_profile}, status=status.HTTP_202_ACCEPTED)
            if  'button2' in request.POST:
                return render(request, "planepdf.html", {'user_profile':user_profile}, status=status.HTTP_202_ACCEPTED)
        except ObjectDoesNotExist:
            messages.error(request, 'Invalid Number OR Number Does Not Exist')
            return redirect('listResume')


class updateapplicant(APIView):

    def get(self, request):

        return render(request, 'editapplicant.html')
    



        