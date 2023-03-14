from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from django.contrib.auth.forms import AuthenticationForm


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful.")
			return redirect("index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render(request=request, template_name="core/register.html", context={"register_form": form})


class IndexView(TemplateView):
    template_name = 'core/index.html'


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("main:homepage")
			else:
				messages.error(request, "Invalid username or password.")
		else:
			messages.error(request, "Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="core/login.html", context={"login_form": form})
