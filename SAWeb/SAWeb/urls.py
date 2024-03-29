"""SAWeb URL Configuration

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

from commentAnalysis.views import test, index, all_user_seti_distribution, single_user_seti_distribution
from commentAnalysis.views import score_and_setiscore, about, commentlength_and_setiscore


urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^test', test),
	url(r'^index', index),
	url(r'^alluser', all_user_seti_distribution),
	url(r'^singleuser', single_user_seti_distribution),
	url(r'^score', score_and_setiscore),
	url(r'^comments', commentlength_and_setiscore),
	url(r'^about', about),
]
