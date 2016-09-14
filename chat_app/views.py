from django.shortcuts import render
import django.views.generic
from chat_app.forms import LoginForm, RegistrationForm
from chat_app.models import Credential, BlackList


class RegistrationView(django.views.generic.FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm

    def post(self, request, *args, **kwargs):
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            # user_name = registration_form.cleaned_data['name']
            # user_surname = registration_form.cleaned_data['surname']
            # user_login = registration_form.cleaned_data['login']
            # user_password = registration_form.cleaned_data['password']
            # try:
            #     credential = Credential(name=user_name, surname=user_surname, login=user_login, password=user_password, is_admin=False)
            #     credential.save()
            #     return render(request, 'index.html', {})
            # except Exception:
            #     pass
            registration_form.save()
            return render(request, 'index.html', {})

        return render(request, 'registration.html', {'error': 'error in registration', 'form': RegistrationForm})


class LoginView(django.views.generic.FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        ulogin = request.session.get('user_login')
        is_admin = request.session.get('is_admin')
        if ulogin is not None:
            if is_admin is not None:
                return render(request, 'admin.html', {'user': ulogin})
            ban = BlackList.objects.filter(id_user__login=ulogin).first()
            if ban is None:
                return render(request, 'chat.html', {'user': ulogin})
            else:
                return render(request, 'ban.html', {'user': ulogin})
        else:
            form = self.get_form(LoginView.form_class)
            return render(request, LoginView.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_login = login_form.cleaned_data['login']
            user_password = login_form.cleaned_data['password']
            c = Credential.objects.filter(login=user_login, password=user_password).first()
            if c is not None:
                request.session['user_login'] = user_login
                if c.is_admin:
                    request.session['is_admin'] = True
                    return render(request, 'admin.html', {'user': user_login})
                else:
                    return render(request, 'chat.html', {'user': user_login})
            else:
                return render(request, 'login.html', {'error': 'login incorrect', 'form': LoginForm})
