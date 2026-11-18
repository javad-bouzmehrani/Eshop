from django import forms
from django.core.validators import RegexValidator


# ─── ویجت سفارشی برای type="tel" ─────────────────────────────
class TelInput(forms.TextInput):
    input_type = 'tel'


# ─── اعتبارسنجی‌ها ────────────────────────────────────────────
national_id_validator = RegexValidator(
    regex=r'^\d{10}$',
    message='کد ملی باید ۱۰ رقم باشد.'
)

sheba_validator = RegexValidator(
    regex=r'^\d{24}$',
    message='شماره شبا باید ۲۴ رقم (بدون پیشوند IR) باشد.'
)


class EditProfileForm(forms.Form):
    # ─── اطلاعات هویتی ───────────────────────────────────────
    first_name = forms.CharField(
        label='نام',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'id': 'first_name',
            'autocomplete': 'given-name',
        }),
    )

    last_name = forms.CharField(
        label='نام خانوادگی',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'id': 'last_name',
            'autocomplete': 'family-name',
        }),
    )

    national_id = forms.CharField(
        label='کد ملی',
        max_length=10,
        disabled=True,                       # کاربر نمی‌تواند تغییر دهد
        validators=[national_id_validator],
        widget=forms.TextInput(attrs={
            'class': 'input input--disabled input--icon input--mono',
            'id': 'national_id',
            'dir': 'ltr',
        }),
    )

    birth_date = forms.CharField(
        label='تاریخ تولد',
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input input--icon',
            'id': 'birth_date',
            'dir': 'ltr',
            'placeholder': '۱۳۷۲/۰۵/۱۸',
        }),
    )

    # ─── اطلاعات ارتباطی ─────────────────────────────────────
    phone = forms.CharField(
        label='شماره تلفن همراه',
        max_length=20,
        disabled=True,
        widget=TelInput(attrs={
            'class': 'input input--disabled input--icon input--mono',
            'id': 'phone',
            'dir': 'ltr',
        }),
    )

    email = forms.EmailField(
        label='پست الکترونیک (ایمیل)',
        widget=forms.EmailInput(attrs={
            'class': 'input input--icon',
            'id': 'email',
            'dir': 'ltr',
            'autocomplete': 'email',
        }),
    )

    # ─── حساب بانکی ──────────────────────────────────────────
    sheba = forms.CharField(
        label='شماره شبا (IBAN)',
        max_length=24,
        required=False,
        validators=[sheba_validator],
        widget=forms.TextInput(attrs={
            'class': 'input input--sheba input--mono',
            'id': 'sheba',
            'dir': 'ltr',
            'placeholder': '7801 2000 0000 0123 4567 8901',
        }),
    )