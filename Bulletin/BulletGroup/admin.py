from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Group)
admin.site.register(models.Codes)
admin.site.register(models.User)
admin.site.register(models.Posts)
admin.site.register(models.Media)


'''
bug:
	it's possible for the group to not have a maker if the creation of the group is not completed
'''
