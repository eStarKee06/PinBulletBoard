# imports:
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from . import forms
from . import models
from django.views import View
from django.core import serializers # to change format
import json
from django.views.decorators.csrf import csrf_exempt
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# part1 instance vars:
madeGroup = False
currentGroup = None
group_form = None
codes_form = None
user_form = None
maker_form = None
currentUser = None
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#render the home page: 
def getHome(request):
	#access instance variables
	global madeGroup
	global currentGroup
	global currentUser
	global group_form 
	global codes_form
	global user_form 
	global maker_form 

	# re-initialize
	madeGroup = False
	currentGroup = None
	currentUser=None
	group_form = forms.GroupForm(request.POST)
	codes_form = forms.CodesForm(request.POST)
	user_form = forms.UserForm(request.POST)
	maker_form = forms.UserForm(request.POST)
	return render(request, 'BulletGroup/index.html', {'group_form':group_form, 'codes_form':codes_form, 'maker_form':maker_form, 'user_form':user_form})
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#backend of making a new group
def processGroup(request):
	#access instance variables
	global madeGroup
	global currentGroup
	global group_form
	
	if(request.method == 'POST'):
		group_form = forms.GroupForm(request.POST)
		if(group_form.is_valid() and (models.Group.objects.filter(name=group_form['name'].value()).count() == 0) ):
			currentGroup = group_form.save()
			madeGroup = True
		
		else:
			return HttpResponse("Error: This group is already made. Please try a different name.")
	
	return HttpResponse()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#backend of making new codes
def processCodes(request):
	#access instance variables
	global madeGroup
	global currentGroup
	global codes_form

	if(request.method == 'POST'):
		codes_form = forms.CodesForm(request.POST)
		if(codes_form.is_valid()):
			new_code = codes_form.save(commit=False)

			numCheck = (models.Group.objects.filter(name=currentGroup.name).get()).codes_set.filter(name=new_code.name).count()
			if(madeGroup and (currentGroup != None) and (numCheck == 0)):
				new_code.group = currentGroup
				new_code.save()

				#serialize: changes query set to a format that can be understood by JSON
				code_list = serializers.serialize('json', list((models.Group.objects.filter(name=currentGroup.name).get()).codes_set.all()), fields=('name'))
				return JsonResponse(code_list, safe=False)

			else:
				return HttpResponse("Error: This code is already made. Please try a different code name.")

	return HttpResponse()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#backend of making new maker
def processMaker(request):
	#access instance variables
	global madeGroup
	global currentGroup
	global maker_form
	global currentUser

	codeMatch = False # init codeMatch
	if(request.method == 'POST'):
		maker_form = forms.UserForm(request.POST)
		codeInput = request.POST.get("user-code")
		
		if(maker_form.is_valid() and (codeInput != "")):
			new_maker = maker_form.save(commit=False)
			currGroup = models.Group.objects.filter(name=currentGroup.name).get()
			codeGroupFilter = currGroup.codes_set.filter(name=codeInput)
			codeMatch = (codeGroupFilter.count() == 1) 
				
			if(codeMatch and madeGroup):
				if(codeGroupFilter.get().inUse): # if the code being used is already being used
					return HttpResponse("Error: the code given is being used")
				if (models.User.objects.filter(codes=codeGroupFilter.get()).count() != 0): # these error cases will probably never happen
					return HttpResponse("Error: Someone is already in use of code given") 
				#if(currGroup.user_set.filter(pseudoName=new_maker.pseudoName).count() != 0):
				#	return HttpResponse("Error: Someone is already in use of the pseudoName")
				new_maker.codes = codeGroupFilter.get()
				new_maker.group = currentGroup
				new_maker.maker = True
				new_maker.save()
				
				currentUser = new_maker
				(codeGroupFilter).update(inUse=True)

				#getBulletin(request) # this is not working
			else:
				return HttpResponse("Error: Code does not exist in Group")
	return HttpResponse()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#backend for a user joining a group
def processUser(request): 
	#access instance variables
	global madeGroup
	global user_form
	global currentGroup # recently added
	global currentUser

	existentUser = None
	codeMatch = False # init codeMatch

	if(request.method == 'POST'):
		user_form = forms.UserForm(request.POST)
		codeInput = request.POST.get("user-code-user")
		groupInput = request.POST.get("user-group")
	
		if(user_form.is_valid() ):
			new_user = user_form.save(commit=False)

			if (models.Group.objects.filter(name=groupInput).count() != 0 ):
				currGroup = models.Group.objects.filter(name=groupInput).get()
				currentGroup = currGroup
				codeGroupFilter = currGroup.codes_set.filter(name=codeInput) # we have to get it first

				if((codeGroupFilter.count() == 1) ): # this means that the code exists in group
					try: # case1: this means that the user is already existent
						existentUser = (codeGroupFilter.get()).user	
						if(codeGroupFilter.get().inUse):
							return HttpResponse("Error: the code given is being used")
						
						if( (models.User.objects.filter(pseudoName=new_user.pseudoName).count() != 0) and (new_user.pseudoName != existentUser.pseudoName) and
						(models.User.objects.filter(pseudoName=new_user.pseudoName).get()).group == currentGroup):
							return HttpResponse("Error: pseudoName already exist")
						
						existentUser.pseudoName = new_user.pseudoName
						existentUser.save()

						#can't be used because code is being used
						currentUser = existentUser
						(codeGroupFilter).update(inUse=True)

					except: # case2: this means that it's a new User'
						if(codeGroupFilter.get().inUse):
							return HttpResponse("Error: the code given is being used")
						
						if( models.User.objects.filter(pseudoName=new_user.pseudoName).count() != 0 and 
						(models.User.objects.filter(pseudoName=new_user.pseudoName).get()).group == currentGroup):
							return HttpResponse("Error: pseudoName already exist")
						
						new_user.codes = codeGroupFilter.get()
						new_user.group = currGroup
						new_user.maker = False
						new_user.save()

						#can't be used because code is being used
						currentUser=new_user
						(codeGroupFilter).update(inUse=True)

				else:
					return HttpResponse("Error: Code does not exist in Group")

			else:
				return HttpResponse("Error: Group does not exist")

		else:
			currentGroup = models.Group.objects.filter(name=groupInput).get()
			currentUser = ((models.Group.objects.filter(name=groupInput).get()).codes_set.filter(name=codeInput)).get().user

	return HttpResponse()

#----------------------------------------------------------------------------------2nd part: Posts------------------------------------------------------------
#instance vars:
posts_form = None
media_form = None
currentPost = None
#-------------------------------------------------------------------------------------------

# checks if user is the maker:
def initializeUser(request):
	#access instance variables
	global currentUser 

	if (currentUser.maker):
		return HttpResponse("true")
	return HttpResponse("false")
#-----------------------------------------------------------------------------------------

# render the bulletin page:
def getBulletin(request):
	#access instance variables
	global currentGroup 
	global posts_form 
	global media_form
	global currentUser

	#posts:
	posts_form = forms.PostsForm(request.POST)
	media_form = forms.MediaForm(request.POST)

	postList = models.Posts.objects.filter(uploader__group = currentGroup).order_by('-date')

	# later add a case to if currentGroup = None; in the case that people just input the url directly
	if(currentGroup != None):
		codeList = currentGroup.codes_set.all()
	return render(request, 'BulletGroup/bulletin.html', {'currentGroup': currentGroup, 'posts_form':posts_form, 'media_form':media_form,
	"currentUser": currentUser, "postList" : postList })
#-----------------------------------------------------------------------------------------

#if maker deletes the group
def deleteGroup(request):
	#access instance variables
	global currentGroup 
	global currentUser

	if(currentGroup != None and currentUser.maker):
		currentGroup.deleteChildren()
		currentGroup.delete() # delete ourselves

	return HttpResponse()
#-----------------------------------------------------------------------------------------

#list codes to select which ones to delete
def listCodes(request):
	#access instance variables
	global currentGroup

	if(currentGroup != None):
		code_list = serializers.serialize('json', list((models.Group.objects.filter(name=currentGroup.name).get()).codes_set.exclude(user__maker=True)), fields=('name'))
		return JsonResponse(code_list, safe=False)
	return HttpResponse()
#-----------------------------------------------------------------------------------------

#if maker deletes codes:
@csrf_exempt
def deleteCodes(request):
	#access instance variables
	global currentGroup 
	global currentUser

	codeListDelete = request.POST.getlist('data[]')
	print(codeListDelete[0])
	if(currentGroup != None and currentUser.maker):
		for i in range(len(codeListDelete)):
			models.Codes.objects.filter(name=codeListDelete[i]).get().deleteChildren()
			models.Codes.objects.filter(name=codeListDelete[i]).get().delete()
			#note to self: figure out later what to do if user is in board but the code is deleted
	return HttpResponse()

#------------------------------------------------------------------posts---------------------------------------------------------------------------------------

#user is making a post
@csrf_exempt
def makePost(request):
	#access instance variables
	global currentUser
	global posts_form 
	global media_form
	global currentPost
	global currentGroup

	if(currentUser == None): #error
		return HttpResponse ("Error: You've been disconnected")

	if(request.method == 'POST'):
		posts_form = forms.PostsForm(request.POST)
		print(request.FILES)
		if(posts_form.is_valid()):
			print(request.POST.get("content"))
			new_post = posts_form.save(commit=False)
			new_post.uploader = currentUser
			print(currentUser)
			new_post.save()
			currentPost = new_post
		else:
			return HttpResponse("Title is necessary")

	return HttpResponse()
#----------------------------------------------------------------------------------

#user is adding a file
def addFile(request):
	#access instance variables
	global media_form
	global posts_form 
	global currentPost

	if(request.method == 'POST'):
		media_form = forms.MediaForm(request.POST, request.FILES)
		if(media_form.is_valid() and (currentPost != None)):
			media_post = media_form.save(commit=False)
			media_post.post = currentPost
			media_post.save()
			media_form = forms.MediaForm(request.POST, request.FILES)
	return HttpResponse()
#----------------------------------------------------------------------------------

#user logs out so that other people can use the code
def logOut(request):
	global currentUser
	models.Codes.objects.filter(user=currentUser).update(inUse=False)
	return HttpResponse()