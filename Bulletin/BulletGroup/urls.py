""" urls.py in BulletGroup; reflects functions from views of BulletGroup and sends it to root"""

from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
	path('', views.getHome), # home page
	path('process-group', views.processGroup), 
	path('process-codes', views.processCodes),
	path('process-maker', views.processMaker), 
	path('process-user', views.processUser),
	#second part
	path('bulletin', views.getBulletin),
	path('delete-group', views.deleteGroup),
	path('list-codes', views.listCodes),
	path('delete-codes', views.deleteCodes),
	path('initialize-user', views.initializeUser),
	path('make-post', views.makePost),
	path('add-file', views.addFile),
	path('log-out', views.logOut)

]
