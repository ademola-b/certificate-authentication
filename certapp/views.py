import qrcode
from io import BytesIO
import base64
from random import choice, shuffle

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from . forms import LoginForm, GenerateCertificateForm, AuthFillForm
from . models import Certificate, Department, Signature

# Create your views here.
def _serial_no():
   
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    comb = ['F', 'P', 'B', '2023']

    [comb.append(choice(numbers)) for _ in range(3)]

    shuffle(list(comb))
    serial_no = ''.join(comb)

    return serial_no


def generate_serial_no():
    exists = True
    appl = None
    while exists:
        appl = _serial_no()
        if not Certificate.objects.filter(serial_number=appl).exists():
            exists = False
    return appl

class HomePageView(TemplateView):
    template_name = "index.html"

class LoginView(View):
    template_name = "auth/login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser and user.is_active:
                    login(request, user)
                    return redirect('auth:dashboard')
                # else:
                #     messages.error(request, "Your account is not active, kindly contact the admin")
            else:
                messages.error(request, "Account not found")
        else:
            messages.error(request, f"An error occurred: {form.errors.as_text()}")
        
        return render(request, self.template_name, {'form':form})

class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(
            request, 'You have successfully logged out, login again to continue')
        return redirect('auth:login')

class DashboardView(View):
    def get(self, request):
        generated_cert = Certificate.objects.count()
        departments = Department.objects.count()
        return render(request, "auth/dashboard.html", {'certs':generated_cert, 'depts': departments})
    
class GenerateCertificateView(View):
    def get(self, request):
        form = GenerateCertificateForm()
        return render(request, "cert/generate_certificate.html", {'form':form})
    
    def post(self, request):
        form = GenerateCertificateForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()

            certificate = Certificate.objects.create(
                serial_number = generate_serial_no(),
                holder = instance,
                issue_date = form.cleaned_data['issue_date']
            )
            messages.success(request, "Certificate Successfully Generated")
            
            qr_image = qrcode.make(f'{settings.REDIRECT_DOMAIN}authenticate-certificate/scanned-result/{certificate.serial_number}/', box_size=2)
            # qr_image = qrcode.make(certificate.serial_number, box_size=5)
            qr_image_pil = qr_image.get_image()
            stream = BytesIO()
            qr_image_pil.save(stream, format='PNG')
            qr_image_data = stream.getvalue()
            qr_image_base64 = base64.b64encode(qr_image_data).decode('utf-8')

            certificate.qr_code = qr_image_base64
            certificate.save()

            signature = Signature.objects.first()
            certificate_data = {
                'first_name' : certificate.holder.first_name,
                'last_name' : certificate.holder.last_name,
                'department': certificate.holder.department.name,
                'level': certificate.holder.level,
                'grade': certificate.holder.grade,
                'picture': certificate.holder.picture,
                'serial_no': certificate.serial_number,
                'serial_number': certificate.serial_number,
                'date': certificate.issue_date,
                'qr_code': qr_image_base64,
                'signature': signature

            }
            return render(request, "cert/certificate.html", certificate_data)
        else:
            messages.error(request, f"An error occured: {form.errors.as_text()}")
        return render(request, "cert/generate_certificate.html", {'form':form})

class AuthenticateCertificateView(View):
    def get(self, request):
        form = AuthFillForm()
        return render(request, "cert/authenticate_certificate.html", {'form':form})
    
    def post(self, request):
        form = AuthFillForm(request.POST)
        if form.is_valid():
            matric_no = request.POST.get('matric_no')
            try:
                cert = Certificate.objects.get(holder__matric_no = matric_no)
                signature = Signature.objects.first()
                return render(request, "cert/cert_with_matric.html", {'cert':cert, 'signature':signature})
            except:
                messages.warning(request, "NO Certificate with the provided matriculation number")
                return render(request, "cert/authenticate_certificate.html", {'form':form})
 
class ScannerView(TemplateView):
    template_name = 'cert/scanner.html'

class ScannedResultView(View):
    def get(self, request, content):
        serial_number = self.kwargs.get('serial')

        try:
            if serial_number is not None:
                certificate = Certificate.objects.get(serial_number = serial_number)
                signature = Signature.objects.first()
                return render(request, "cert/scanned_result.html", {'cert':certificate, 'signature':signature})
            else:
                certificate = Certificate.objects.get(serial_number = content)
                certificate = Certificate.objects.get(serial_number = content)
                signature = Signature.objects.first()
                return render(request, "cert/scanned_result.html", {'cert':certificate, 'signature':signature})
        except Certificate.DoesNotExist:
            return render(request, "cert/scanned_result.html")
