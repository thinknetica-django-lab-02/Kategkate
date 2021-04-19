"""bookme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from posts import views
from django.conf.urls import url, include
from django.contrib import admin
from posts.views import AboutView, ContactView, ExperienceView, NewsroomView

from posts.views import ApartListView, ApartDetailView, ApartmentCreateView, ApartmentEditView

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('about/', AboutView.as_view()),
    path('contact/', ContactView.as_view()),
    path('experience/', ExperienceView.as_view()),
    path('newsroom/', NewsroomView.as_view()),
    path('apartment/', ApartListView.as_view(), name='apartment'),
    path('apartment/<pk>', ApartDetailView.as_view()),
    path('accounts/', include('accounts.urls')),
    path('apartment/create/', ApartmentCreateView.as_view(), name='apartment-create'),
    path('apartment/<pk>/edit/', ApartmentEditView.as_view(), name='apartment-edit'),
    path('accounts/', include('allauth.urls')),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
