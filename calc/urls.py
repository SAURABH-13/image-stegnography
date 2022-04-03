from django.urls import path
from django.contrib import admin
from django.conf import settings 
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.home,name = 'home'),
    path('home',views.home,name = 'home'),
    path('dectimage',views.dectimage, name = 'dectimage'), 
    path('showimage',views.showimage, name = 'showimage'), 
    path('browse1',views.browse1, name = 'browse1'), 
    path('feat',views.feat, name = 'feat'),
    path('test_res',views.test_res, name = 'test_res'),
    
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)