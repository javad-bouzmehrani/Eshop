from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Login(forms.Form):
    username = forms.CharField(
        label='شماره موبایل',
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message='شماره موبایل باید ۱۱ رقم باشد'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'input input-ltr',
            'placeholder': '09123456789',
            'dir': 'ltr',
            'id': 'login-identifier',
            'inputmode': 'numeric',
            'maxlength': '11',
            'autocomplete': 'username',
        })
    )

    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'input input-ltr input-pass',
            'placeholder': '••••••••',
            'id': 'login-password',
            'autocomplete': 'current-password',
        })
    )

class Register(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'name': 'full_name',
            'id': 'reg-name',
            'placeholder': 'مثال: علی رضایی',
            'class': 'input',
            'autocomplete': 'name',
        })
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'tel',
            'name': 'phone',
            'id': 'reg-phone',
            'dir': 'ltr',
            'placeholder': '09xxxxxxxxx',
            'class': 'input input-ltr',
            'inputmode': 'numeric',
            'maxlength': '11',
            'autocomplete': 'tel',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'name': 'password',
            'id': 'reg-password',
            'dir': 'ltr',
            'placeholder': 'حداقل ۸ کاراکتر ترکیبی',
            'class': 'input input-ltr input-pass',
            'autocomplete': 'new-password',
        })
    )
    agree = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'name': 'agree',
            'class': 'checkbox checkbox-mt',
        })
    )

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if len(full_name.strip()) < 3:
            raise forms.ValidationError("نام و نام خانوادگی باید حداقل ۳ کاراکتر باشد")
        return full_name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("شماره موبایل باید فقط شامل اعداد باشد")
        if len(phone) != 11:
            raise forms.ValidationError("شماره موبایل باید ۱۱ رقم باشد")
        if not phone.startswith('09'):
            raise forms.ValidationError("شماره موبایل باید با ۰۹ شروع شود")
        if User.objects.filter(username=phone).exists():
            raise forms.ValidationError("این شماره موبایل قبلاً ثبت شده است")
        return phone

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("کلمه عبور باید حداقل ۸ کاراکتر باشد")
        return password

    def clean_agree(self):
        agree = self.cleaned_data.get('agree')
        if not agree:
            raise forms.ValidationError("پذیرش قوانین و مقررات الزامی است")
        return agree
