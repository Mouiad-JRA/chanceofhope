from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import CreateView, FormView, RedirectView

from account.forms import UserCreationForm, UserLoginForm
from account.models import CustomUser


class UserRegistrationView(CreateView):
    """
        Provides the ability to register as a Patient.
    """
    model = CustomUser
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('account:user-login')
        else:
            return render(request, 'accounts/register.html', {'form': form})


class LoginView(FormView):
    success_url = '/'
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    extra_context = {
        'title': 'login'
    }

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)

        # Check here if the user is an admin
        if user is not None and user.is_active:
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)
        else:
            return self.form_invalid(form)


class LogoutView(RedirectView):
    """
        Provides users the ability to logout
    """
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out from My site :)')
        return super(LogoutView, self).get(request, *args, **kwargs)
