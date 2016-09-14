from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from chat_app.views import RegistrationView, LoginView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^registration$', RegistrationView.as_view()),
    url(r'^registration_handler$', RegistrationView.as_view()),
    url(r'^login$', LoginView.as_view()),
    url(r'^login_handler$', LoginView.as_view()),
]
