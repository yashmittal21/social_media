from django.db import models

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length = 100)
	password = models.CharField(max_length= 100)
	email = models.EmailField()
	follower = models.IntegerField(default=0)
	following = models.IntegerField(default=0)
	isSuperAdmin = models.BooleanField()

	def __str__(self):
		return self.name

class Post(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	time = models.TimeField(auto_now=True)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	like = models.IntegerField(default=0)

class Comment(models.Model):
	desc = models.TextField()
	post = models.ForeignKey(Post, on_delete = models.CASCADE)