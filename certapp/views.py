import qrcode
from io import BytesIO
import base64
from random import choice, shuffle

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from . forms import LoginForm, GenerateCertificateForm
from . models import Certificate

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

class DashboardView(View):
    def get(self, request):
        return render(request, "auth/dashboard.html")
    
class GenerateCertificateView(View):
    def get(self, request):
        form = GenerateCertificateForm()
        return render(request, "cert/generate_certificate.html", {'form':form})
    
    def post(self, request):
        form = GenerateCertificateForm(request.POST)
        if form.is_valid():
            instance = form.save()

            # form.save()
            certificate = Certificate.objects.create(
                serial_number = generate_serial_no(),
                holder = instance
            )
            messages.success(request, "Certificate Successfully Generated")

            qr_image = qrcode.make(certificate.serial_number, box_size=15)
            qr_image_pil = qr_image.get_image()
            stream = BytesIO()
            qr_image_pil.save(stream, format='PNG')
            qr_image_data = stream.getvalue()
            qr_image_base64 = base64.b64encode(qr_image_data).decode('utf-8')
            
            # qr = qrcode.QRCode(
            #     version=1,
            #     error_correction=qrcode.constants.ERROR_CORRECT_L,
            #     box_size=10,
            #     border=4,
            # )
            # qr.add_data(certificate.serial_number)  # Adjust this URL based on your certificate viewing URL
            # qr.make(fit=True)

            # img = qr.make_image(fill_color="black", back_color="white")

            # # Create a BytesIO object to store the image
            # qr_image = BytesIO()
            # img.save(qr_image, "PNG")
            # qr_image.seek(0)


            certificate_data = {
                'first_name' : certificate.holder.first_name,
                'last_name' : certificate.holder.last_name,
                'department': certificate.holder.department.name,
                'grade': certificate.holder.grade,
                'serial_number': certificate.serial_number,
                'qr_code': qr_image_base64
            }
            return render(request, "cert/certificate.html", certificate_data)
        else:
            messages.error(request, f"An error occured: {form.errors.as_text()}")
        return render(request, "cert/generate_certificate.html", {'form':form})

class AuthenticateCertificateView(View):
    def get(self, request):
        return render(request, "cert/authenticate_certificate.html")
    
class ScannerView(TemplateView):
    template_name = 'cert/scanner.html'

class ScannedResultView(View):
    def get(self, request, content):
        try:
            certificate = Certificate.objects.get(serial_number = content)
            return render(request, "cert/scanned_result.html", {'cert':certificate})
        except Certificate.DoesNotExist:
            return render(request, "cert/scanned_result.html")
