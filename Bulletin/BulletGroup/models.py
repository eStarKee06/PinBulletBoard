from django.db import models

'''
	Group
		name: name of the group
	Functions
		deleteChildren: if Group is deleted, everything will be deleted
'''
class Group(models.Model):
	name = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return (self.name)

	def deleteChildren(self):
		for code in self.codes_set.all():
			try:
				code.user.deleteChildren() # additional => only if group is deleted; if codes are deleted, let the posts be ownerless
			except: 
				pass
			code.deleteChildren()
			code.delete()

'''
	Codes
		name: name of the code
		group: name of the group that it belongs in
	Functions
		deleteChildren: if the code is deleted, the user using it will also be deleted
'''		
class Codes(models.Model):
	name = models.CharField(max_length=20)
	group = models.ForeignKey('Group', on_delete=models.CASCADE)
	inUse = models.BooleanField(default=False)
	
	def __str__(self):
		return (self.name)

	def	deleteChildren(self):
		try:
			self.user.delete()
		except:
			pass

'''
	User
		maker: determines if maker privilege exists
		codes: pass code to join the group
		pseudoName: the name that will be used by user within the group
		group: the group that the user wants to join
	Functions
		deleteChildren: to delete posts under the user, used when the whole group is deleted
'''		
class User(models.Model):
	maker = models.BooleanField(default=False)
	codes = models.OneToOneField('Codes', on_delete=models.CASCADE, related_name = "user")
	pseudoName = models.CharField(max_length=20,  unique=False)
	group = models.ForeignKey('Group', on_delete=models.CASCADE)

	def __str__(self):
		return (self.pseudoName)

	# if group is deleted, all the posts will be deleted 
	def deleteChildren(self):
		for posts in self.posts_set.all():
			posts.deleteChildren()
			posts.delete()


#----------------------------------------------------------------2nd part---------------------------------------------------------------------------
'''
	Posts
		uploader: the user that made the post
		date: the date that the post is made
		title: the title of the post
		freewrite: the body of the post
	funtions
		deleteChildren: delete any media under the post
'''	
class Posts(models.Model):
	uploader = models.ForeignKey('User', on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now=True)
	title =  models.CharField(max_length=100)
	freeWrite =  models.TextField(blank=True)

	# if group is deleted, all the posts will be deleted 
	def deleteChildren(self):
		for media in self.media_set.all():
			media.delete()

'''
	Media
		content: the file that will be uploaded
		post: the post that the file belongs to 
'''
class Media(models.Model):
	content = models.FileField() 
	post = models.ForeignKey('Posts', on_delete=models.CASCADE)