#handles making making of model obj
from django.forms import ModelForm
from django import forms
from . import models

#form for Group model
class GroupForm(ModelForm):
	class Meta:
		model = models.Group
		fields = ['name']
		widgets = {
			'name':forms.TextInput(attrs={
				"placeholder": 'group name',
				"class" : 'group-form'
				#'required': True 
            })
		}

#form for User model
class UserForm(ModelForm):
	class Meta:
		model = models.User
		fields = ['pseudoName']
		widgets = {
			'pseudoName':forms.TextInput(attrs={
				'id': 'user-pseudo-name',
				"placeholder": 'pseudo-name',
				"class" : 'user-form'
				#'required': True 
            }) 
		}
			
#form for Codes model
class CodesForm(ModelForm):
	class Meta:
		model = models.Codes
		fields = ['name']
		widgets = {
			'name':forms.TextInput(attrs={
				'id': 'code-name',
				"class" : 'codes-form',
				"placeholder": 'code name',
				'required': True 
            })
		}

#form for Posts model
class PostsForm(ModelForm):
	class Meta:
		model = models.Posts
		fields = ['title', 'freeWrite']
		widgets = {
			'title':forms.TextInput(attrs={
				'class': 'title-name',
				'placeholder': 'Title of Post'
            }),
			'freeWrite':forms.Textarea(attrs={
				'class': 'post-body',
				'placeholder': 'Text Body'
            })
		}

#form for Media model
class MediaForm(ModelForm):
	class Meta:
		model = models.Media
		fields = ['content']
	