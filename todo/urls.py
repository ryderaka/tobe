"""todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from tobe.views import otp_generate, otp_verify, get_profile, new_profile, create_todo, accept_todo, dashboard

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^phone/', otp_generate),
    url(r'^otpverify/', otp_verify),
    url(r'^register/', new_profile),
    url(r'^profile/', get_profile),
    url(r'^createtask/', create_todo),
    url(r'^dashboard/', dashboard),
    url(r'^accepttask/', accept_todo),
]
