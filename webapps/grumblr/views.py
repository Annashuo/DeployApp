from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.db import transaction
from grumblr.models import *
from grumblr.forms import *

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm

from django.contrib.auth import authenticate, login as auth_login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from operator import attrgetter
from mimetypes import guess_type
from django.core.mail import send_mail, EmailMessage
from django.utils import timezone
from django.utils.crypto import get_random_string

import hashlib

def login(request):
	if request.method == 'GET':
		if request.user.is_authenticated and request.user.is_active:
			auth_login(request, request.user)
			return redirect('home')
	error = ''
	form = AuthenticationForm()
	form.fields['username'].widget.attrs['placeholder'] = 'Username'
	form.fields['password'].widget.attrs['placeholder'] = 'Password'
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		form.fields['username'].widget.attrs['placeholder'] = 'Username'
		form.fields['password'].widget.attrs['placeholder'] = 'Password'
		if form.is_valid():
			user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
			if user.is_active:
				auth_login(request, user)
				return redirect('home')
		else:
			error = 'Wrong username or password.'
	return render(request, 'grumblr/login.html', {'form':form, 'error':error})

def signup(request):
	if request.user.is_authenticated():
		return redirect('home')
	if request.method == "GET":
		context = {'form':RegistrationForm()}
		return render(request, 'grumblr/signup.html', context)

	form = RegistrationForm(request.POST)

	if not form.is_valid():
		context = {'form':form}
		return render(request,'grumblr/signup.html', context)

	new_user = User.objects.create_user(email=form.cleaned_data['email'],\
		username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
	new_user.is_active = False
	new_user.save()

	new_user_profile = UserProfile(user=new_user, first_name=form.cleaned_data['firstname'],\
		last_name=form.cleaned_data['lastname'])
	new_user_profile.save()

	token = default_token_generator.make_token(new_user)
	email_body = """
	Welcome to Grumblr. Please click the link below to verify your email address
	http://%s%s
	""" %(request.get_host(),
		reverse('activation', args=(new_user.username, token)))

	send_mail(subject='Verify your email address.',
		message=email_body,
		from_email='shuoh1@andrew.cmu.edu',
		recipient_list=[new_user.email])

	context = {'email':form.cleaned_data['email']}
	return render(request,'grumblr/need_confirmation.html', context)
	

def activation(request, username, token):
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, token):
    	user.is_active=True
    	user.save()
    	auth_login(request,user)
    	return redirect('home')
    else:
    	return HttpResponse("Verify your email fail.")


@login_required
@transaction.atomic
def profile(request, current_user):
	cuser = get_object_or_404(User, username=current_user)
	currentuser = UserProfile.objects.get(user = cuser)
	user = request.user
	items = Post.get_posts(user=cuser)

	if request.method == 'POST':
		try:
			has_follow = Follow.objects.get(owner=request.user, follow=cuser)
			has_follow.delete()
			followbutton = 'Follow'
		except ObjectDoesNotExist:
			new_follow = Follow(owner=request.user, follow=cuser)
			new_follow.save()
			followbutton = 'Unfollow'
	else:
		try:
			has_follow = Follow.objects.get(owner=request.user, follow=cuser)
			followbutton = 'Unfollow'
		except ObjectDoesNotExist:
				followbutton = 'Follow'
	context = {'current_user':currentuser, 'user':user,'items':items, 'followbutton':followbutton}
	return render(request, 'grumblr/profile.html', context)


@login_required
@transaction.atomic
def home(request):
	error = ''
	form = PostForm()
	if request.method == 'POST':
		new_post = Post(user=request.user)
		form = PostForm(request.POST, instance = new_post)
		if form.is_valid():
			form.save()
		error = form.errors
	items = Post.objects.all().order_by('-time')
	context = {'form':form, 'error':error, 'user':request.user, 'items':items}
	return render(request, 'grumblr/global.html', context)

@login_required
def myfollow(request):
	items = Post.objects.none()
	all_follow = Follow.objects.filter(owner=request.user)
	if all_follow.exists():
		for afollow in all_follow:
			alist = Post.get_posts(user=afollow.follow)
			items |= alist 
		items = items.order_by('-time')
	context = {'user':request.user, 'items':items}
	return render(request, 'grumblr/follow.html', context)

@login_required
@transaction.atomic
def editprofile(request):
	profile_to_edit = get_object_or_404(UserProfile, user=request.user)
	form = ProfileForm(instance=profile_to_edit)
	if request.method == 'POST':
		form = ProfileForm(request.POST, request.FILES ,instance=profile_to_edit)
		if form.is_valid():
			form.save()
			return redirect('profile', request.user.username)

	cuser = request.user
	currentuser = UserProfile.objects.get(user = cuser)
	user = request.user
	items = Post.get_posts(user=request.user)
	context = {'current_user':currentuser, 'user':user,'items':items,'form':form}

	return render(request, 'grumblr/edit.html', context)

@login_required
@transaction.atomic
def change_password(request):
	if request.method == 'POST':
		passwordform = PasswordChangeForm(request.user, request.POST)
		if passwordform.is_valid():
			user = passwordform.save()
			update_session_auth_hash(request, user)  # Important!
			return redirect('profile', request.user.username)

	else:
		passwordform = PasswordChangeForm(request.user)
	cuser = request.user
	currentuser = UserProfile.objects.get(user = cuser)
	user = request.user
	items = Post.get_posts(user=request.user)
	context = {'current_user':currentuser, 'user':user,'items':items,'passwordform':passwordform}

	return render(request, 'grumblr/edit.html', context)
	

@login_required
def get_photo(request, current_user):
	user = User.objects.get(username=current_user)
	entry = get_object_or_404(UserProfile, user=user)
	if not entry.photo:
		entry.photo = "photos/no-user-image.gif"

	content_type = guess_type(entry.photo.name)
	return HttpResponse(entry.photo, content_type=content_type)

@login_required
@transaction.atomic
def delete_item(request, item_id):
	errors = ''
	try:
		item_to_delete = Post.objects.get(id=item_id)
		item_to_delete.delete()
	except ObjectDoesNotExist:
		error = 'The item did not exit.'

	return redirect('editprofile')

def get_changes(request, time="1970-01-01T00:00+00:00"):
	max_time = Post.get_max_time()
	items = Post.get_items(time)
	context = {"max_time":max_time, "items":items} 
	return render(request, 'grumblr/items.json', context, content_type='application/json')
  

def comment(request, item_id, time="1970-01-01T00:00+00:00"):
	if 'time' in request.GET and request.GET['time']:
		time = request.GET['time']
	print(time)
	max_time = Comment.get_max_time(int(item_id))
	items = Comment.get_comments(itemid=int(item_id), time=time)
	context = {"max_time":max_time, "items":items}
	return render(request, 'grumblr/comments.json', context, content_type='application/json')

def addcomment(request, item_id):
	if not 'comment' in request.POST or not request.POST['comment']:
		raise Http404
	else:
		new_comment = Comment(itemid=item_id, comment_owner=request.user, content=request.POST['comment'])
		new_comment.save()
	return HttpResponse("")
