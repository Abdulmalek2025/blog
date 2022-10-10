from django.shortcuts import render
from .forms import RegisterUserForm, ProfileForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        profile_form = ProfileForm(request.POST,request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password2'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return render(request,'account/register_done.html',{'user':user})
    else:
        form = RegisterUserForm()
        profile_form = ProfileForm()
    return render(request,'account/register.html',{'form':form,'profile_form':profile_form})
