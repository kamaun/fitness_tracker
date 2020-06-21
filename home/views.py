from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse, get_list_or_404, get_object_or_404, redirect
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.views.decorators.clickjacking import xframe_options_sameorigin, xframe_options_exempt


def home(request):
    return render(
        request=request,
        template_name='main/home.html'
    )

