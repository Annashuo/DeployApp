from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Max
from django.utils.html import escape

class Post(models.Model):
	user = models.ForeignKey(User)
	content = models.CharField(max_length=42)
	time = models.DateTimeField(default=timezone.now)
	def __unicode__(self):
		return self
	@staticmethod
	def get_posts(user):
		return Post.objects.filter(user=user).order_by('-time')

	@staticmethod
	def get_items(time="1970-01-01T00:00+00:00"):
		return Post.objects.filter(time__gt=time).distinct().order_by('-time')

	@staticmethod
	def get_max_time():
		return Post.objects.all().aggregate(Max('time'))['time__max'] or "1970-01-01T00:00+00:00"

	def html(self):
		str1 = "%s" % escape(self.user.username)
		str_content = "%s" % escape(self.content)
		str_time = "%s" % (timezone.localtime(self.time).strftime('%Y-%-m-%-d %H:%M:%S'))
		time2 = "%s" % (self.time)
		itemid = "%d" % (self.id)
		str2 = "<div class='hero-unit' id='"
		str10 = "'><div class='media'><a class='pull-left' href='/profile/"
		str3 = "'><img class='media-object img-circle' src='/photo/"
		str4 = "'></a><div class='pull-left media-body' ><a class='pull-left' href='/profile/"
		str5 = "'><p>"
		str6 = ": </p></a><p class='pull-left'>"
		str7 = "</p></div><p class='pull-right time' id='"
		str8 = "'>"
		str9 = "</p><button class='pull-right comment' id='comment'>comment</button></div><div id='commentplace'></div></div>"

		return str2+itemid+str10+str1+str3+str1+str4+str1+str5+str1+str6+str_content+str7+ time2+str8+str_time+str9
		

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	first_name = models.CharField(max_length=200, default="", blank=True)
	last_name = models.CharField(max_length=200, default="", blank=True)
	age = models.CharField(max_length=3, default="", blank=True)
	bio = models.CharField(max_length=420, default="", blank=True)
	photo = models.ImageField(upload_to="photos", blank=True)

	def __unicode__(self):
		return self
		
class Follow(models.Model):
	owner = models.ForeignKey(User, null=True, related_name='owner')
	follow = models.ForeignKey(User, null=True, related_name='follow')

class Comment(models.Model):
	itemid = models.IntegerField();
	comment_owner = models.ForeignKey(User, related_name='comment_owner')
	content = models.CharField(max_length=42)
	time = models.DateTimeField(default=timezone.now)
	@staticmethod
	def get_max_time(itemid):
		return Comment.objects.filter(itemid=itemid).aggregate(Max('time'))['time__max'] or "1970-01-01T00:00+00:00"

	@staticmethod
	def get_comments(itemid, time="1970-01-01T00:00+00:00"):
		return Comment.objects.filter(itemid=itemid, time__gt=time).distinct().order_by('time')

	def html(self):
		str1 = "%s" % escape(self.comment_owner.username)
		str_content = "%s" % escape(self.content)
		str_time = "%s" % (timezone.localtime(self.time).strftime('%Y-%m-%d %H:%M:%S'))
		str2 = "<div class='hero-unit'><div class='media'><img class='pull-left media-object img-circle' src='/photo/"
		str4 = "'><div class='pull-left' ><p>"
		str6 = ": "
		str7 = "</p></div><p class='pull-right commenttime'>"
		str8 = "</p></div></div>"

		return str2+str1+str4+str1+str6+str_content+str7+str_time+str8

		