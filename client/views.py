from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

# Create your views here.


def register(request):

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data['username']
            messages.success(request, f'Your account has been created')
            return redirect('home:home')

    else:
        register_form = RegisterForm()

    return render(
        request=request,
        template_name='client/register.html',
        context={
            'title': 'Client Registration',
            'register_form': register_form
        }
    )
