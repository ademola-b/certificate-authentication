from django import forms
from django.contrib.auth.forms import AuthenticationForm

from . models import Department, Course

from . models import Holder
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'id': 'exampleInputEmail1','class':'form-control form-control-lg', 'placeholder':'Username', 'autofocus': 'true'}))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'id':'exampleInputPassword1','class':'form-control form-control-lg', 'placeholder':'Password'}))


class GenerateCertificateForm(forms.ModelForm):

    email = forms.CharField(help_text='Enter email', widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg input-lg',
            'type': 'email',
        }
    ))

    first_name = forms.CharField(help_text='Enter first name', widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg input-lg',
        }
    ))
    last_name = forms.CharField(help_text='Enter first name', widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg input-lg',
        }
    ))
    matric_no = forms.CharField(help_text='Enter first name', widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg input-lg',
        }
    ))

    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="--Select Department--", required=True, help_text="Select department",  widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    picture = forms.ImageField(
        required=True, help_text="Student Picture", widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'type': 'file',
                'accept': 'image/jpeg, image/png'
            })
    )

    grade = forms.ChoiceField(
        required=True,
        choices= [
            ('pass', 'pass'),
            ('lower credit', 'lower credit'),
            ('upper credit', 'upper credit'),
            ('distinction', 'distinction')
        ],
        widget=forms.Select(attrs={'class': 'form-control select form-select'})
    )

    level = forms.ChoiceField(
        required=True,
        choices= [
            ('national diploma', 'national diploma'),
            ('higher national diploma', 'higher national diploma'),
        ],
        widget=forms.Select(attrs={'class': 'form-control select form-select'})
    )

    issue_date = forms.DateField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'type': 'date'
            })
    )

    class Meta:
        model = Holder
        fields = "__all__"

class AuthFillForm(forms.Form):
    matric_no = forms.CharField(help_text='matriculation number', widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg input-lg',
            'placeholder': 'Enter matriculation number'
        }
    ))
