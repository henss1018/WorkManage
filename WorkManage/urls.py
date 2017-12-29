"""WorkManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from . import view
from . import testdb


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hello/', view.hello),
    url(r'^testdb/', testdb.testdb),
    url(r'^mydb/', testdb.mydb),
    url(r'^budget_info/',view.budget_info),
    url(r'^contract_info/', view.contract_info),
    url(r'^budget_detail/$', view.budget_info_detail, name='budget_detail'),
    url(r'^contract_order/$', view.contract_order, name='contract_order'),
    url(r'^contract_aeinfo/$', view.contract_aeinfo, name='contract_aeinfo')
]
