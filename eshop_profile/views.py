from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect

from eshop_profile.forms import EditProfileForm


# Create your views here.
@login_required(login_url='/auth')
def profile(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    first_name = user.first_name
    last_name = user.last_name
    email = user.email
    phone_org = user.username

    if phone_org.startswith('0'):
        num = phone_org[1:]
        phone = f'+98 {num[:3]} {num[3:6]} {num[6:]}'
    else:
        phone = phone_org
    context = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone': phone,
    }
    return render(request,'profile/profile.html',context)

@login_required(login_url='/auth')
def edit_profile(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    initial_data = {
        'first_name':  user.first_name,
        'last_name':   user.last_name,
        'national_id': '1051770569',
        'birth_date':  '۱۳۷۲/۰۵/۱۸',
        'phone':       user.username,
        'email':       user.email,
        'sheba':       '',
    }
    if user is None:
        raise Http404()


    form = EditProfileForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        return redirect('profile')

    context = {
        'form': form,
    }
    return render(request,'profile/change_profile.html',context)