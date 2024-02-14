from asyncio import log
from collections import OrderedDict
import datetime
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
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import csv


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

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
            latestindex = '0'
        else:
            latestindex = idlst[-1] + 1

        condata = {
            'ids' : str(latestindex),
        }
        print(condata)

        return render(request, 'registrationform.html', {'context': condata['ids'] })
    
    def post(self, request):

        upfiles = request.FILES.get('Aadhar_card', False)
        upfiles1 = request.FILES.get('Death_certificate', False)
        upfiles2 = request.FILES.get('Other_file', False)


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
                                                Deceased_age=request.data.get('Deceased_age'),
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
                                                Aadhar_card=upfiles,
                                                Death_certificate=upfiles1,
                                                Other_file=upfiles2,
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
                pdf = render_to_pdf('burial.html' ,context)
                if pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = "Form C_%s.pdf" %("contact")
                    content = "inline; filename='%s'" %(filename)
                    download = request.GET.get("download")
                    if download:
                        content = "attachment; filename='%s'" %(filename)
                    response['Content-Disposition'] = content
                    return response
                return HttpResponse("Not found")
                # return HttpResponse(pdf, content_type='application/pdf')
                
                # return render(request, "burial.html", {'user_profile':user_profile}, status=status.HTTP_202_ACCEPTED)
            # html = template.render(context)
            
            if  'button2' in request.POST:
                context1 ={
                     'user_profile':user_profile
                }
                template = get_template('planepdf.html')
                pdf = render_to_pdf('planepdf.html' ,context1)
                if pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = "LetterHead_%s.pdf" %("contact")
                    content = "inline; filename='%s'" %(filename)
                    download = request.GET.get("download")
                    if download:
                        content = "attachment; filename='%s'" %(filename)
                    response['Content-Disposition'] = content
                    return response
                return HttpResponse("Not found")
                # return render(request, "planepdf.html", {'user_profile':user_profile}, status=status.HTTP_202_ACCEPTED)
            
            user_data = metainformation.objects.filter(Contact_number=contact)
            serial = metainfoserializer(user_data, many=True)
            print(serial.data)
            for i in serial.data:
                datea = i.get('Date')
                dod = i.get('Date_of_death')
                tod = i.get('time_of_death')

                if  'button3' in request.POST:
                    return render(request, 'editapplicant.html', {'user_datas':user_data, 'dates': datea, 'dod':dod,'tod':tod}, status=status.HTTP_202_ACCEPTED)
                if 'button4' in request.POST:
                    user_data.delete()
                    messages.success(request, 'Deleted Successful!')
                    return render(request, 'listResume.html', status=status.HTTP_202_ACCEPTED)
        except ObjectDoesNotExist:
            messages.error(request, 'Invalid Number OR Number Does Not Exist')
            return redirect('listResume')
    
class exportdata(APIView):
    def get(self, request):
        return render(request, 'export.html')

class exporttoexcel(APIView):
    
    def post(self,request):
        st_dt = request.POST['startDate']
        ed_dt = request.POST['endDate']
        user_profile = metainformation.objects.all()  
        # if  'button' in request.POST: 
        output_json_list = []
        output_json_n = {}
        count = 0
        for data in user_profile:
            if data.Date is not None:
                dt = str(data.Date)
            else:
                continue

            if st_dt <= dt <= ed_dt:

                keyList = ['USERID','Applicant_name','Deceased_name','Deceased_age','Gender','Contact_number','Address',
                        'Deceased_address','Date','Date_of_death','time_of_death','Cause_of_death','Relationship','Form_number',
                        'Amount','Aadhar_card','Death_certificate','Other_file' ]

                valueList = [
                                str(data.USERID),str(data.Applicant_name),str(data.Deceased_name),str(data.Deceased_age),str(data.Gender),
                                str(data.Contact_number),str(data.Address),str(data.Deceased_address),str(data.Date),str(data.Date_of_death),str(data.time_of_death),
                                str(data.Cause_of_death),str(data.Relationship),str(data.Form_number),str(data.Amount),str(data.Aadhar_card),
                                str(data.Death_certificate),str(data.Other_file)
                            ]

                output_json_n = OrderedDict(zip(keyList, valueList))
                output_json_list.append(output_json_n)
                count =  count + 1


        ## To Download In Browser CSV File   

        filenamedt = datetime.datetime.now()
        now_without_microseconds = filenamedt.replace(microsecond=0)
        file_name = datetime.datetime.strftime(now_without_microseconds, '%Y-%m-%d %H %M %S')
        newfilename = str(file_name) + '.csv'
        fname = f"{newfilename}"
        response = HttpResponse( content_type='text/csv',headers={'Content-Disposition': f'attachment; filename="{fname}"'})
        writer = csv.DictWriter(response, fieldnames=output_json_list[0].keys())
        writer.writeheader()
        for row in output_json_list:
            writer.writerow(row) 
        messages.success(request, 'Data Export Successful!')
        return response

                ## To Download In System CSV File           

                # filenamedt = datetime.datetime.now()
                # now_without_microseconds = filenamedt.replace(microsecond=0)
                # file_name = datetime.datetime.strftime(now_without_microseconds, '%Y-%m-%d %H %M %S')
                # newfilename = str(file_name) + '.csv'
                # with open(str(newfilename), mode='w', newline='') as file:
                #     writer = csv.DictWriter(file, fieldnames=output_json_list[0].keys())
                #     writer.writeheader()
                #     for row in output_json_list:
                #         writer.writerow(row)
                # print(count)
                # print("Data fetched successfully")
                # messages.success(request, 'Data Export Successful Filename ' + str(newfilename))            
                # return Response(output_json_list, status=status.HTTP_200_OK)
    

class updatedetails(APIView):

    def post(self, request, phoneno):

        try:
            data  =   metainformation.objects.get(Contact_number=phoneno)
        except metainformation.DoesNotExist:
            return Response({'error':'Data Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializedata =  metainfoserializer(data, data=request.data, partial=True)
        if serializedata.is_valid():
            serializedata.save()
            messages.success(request, 'Update Successful!' )
            # return Response(serializedata.data)
            return render(request, 'editapplicant.html', status=status.HTTP_200_OK)
        return Response(serializedata.errors, status=status.HTTP_400_BAD_REQUEST)