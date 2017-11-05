from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from grumblr.models import *
from django.core.mail import send_mail

class ResetForm(forms.Form):
	username = forms.CharField(max_length=200,widget=forms.TextInput(attrs = {'placeholder': 'Username'}))
	email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs = {'placeholder': 'Email'}))
	def clean(self):
		cleaned_data = super(ResetForm,self).clean()
		if self.errors:
			raise forms.ValidationError('Email address is invalid.')
		username = self.cleaned_data.get('username')
		email = self.cleaned_data.get('email')
		try:
			user = User.objects.get(username=username, email=email)
			userprofile = UserProfile(user = user)
		except ObjectDoesNotExist:
			raise forms.ValidationError("Wrong username or email.")
		return cleaned_data

		

class RegistrationForm(forms.Form):
	username = forms.CharField(max_length=200,widget=forms.TextInput(attrs = {'placeholder': 'Username'}))
	email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs = {'placeholder': 'Email'}))
	firstname = forms.CharField(max_length=200,widget=forms.TextInput(attrs = {'placeholder': 'Firstname'}))
	lastname = forms.CharField(max_length=200,widget=forms.TextInput(attrs = {'placeholder': 'Lastname'}))
	password1 = forms.CharField(max_length=200,widget=forms.PasswordInput(attrs = {'placeholder': 'Password'}))
	password2 = forms.CharField(max_length=200,widget=forms.PasswordInput(attrs = {'placeholder': 'Confirm Password'}))

	def clean(self):
		cleaned_data = super(RegistrationForm, self).clean()
		if self.errors:
			raise forms.ValidationError('Email address is invalid.')
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact=username):
			raise forms.ValidationError("Username is already taken.")

		if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
			raise forms.ValidationError("Different password and confirm password");
		return cleaned_data
			
class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = {'content',}
		widgets = {'content': forms.Textarea(attrs = {'placeholder': 'Less than 42 characters', 'rows':'1','style':'width:98%;'})}
			

class ProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['first_name', 'last_name','age', 'bio', 'photo']
		widgets = {'photo':forms.FileInput(), 
					'bio':forms.Textarea(attrs={'row':'1'})}
	
class FollowForm(forms.Form):
	follow = forms.CharField(max_length=2, widget=forms.HiddenInput(attrs={'value':'1'}))
		
			
		
		
	
		
		
			
