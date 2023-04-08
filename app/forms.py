from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MyProfile , Job, Skills , Company , StartUps

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2","first_name","last_name")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class ProfileForm(forms.ModelForm):
	class Meta:
		model = MyProfile
		exclude = ('user','is_active')	

	def __init__(self, *args, **kwargs):
		skills = Skills.objects.all()
		super().__init__(*args, **kwargs)
		self.fields['skills'].widget.attrs={'class':'select2'}	

	
class PostJobForm(forms.ModelForm):
	class Meta:
		model = Job
		exclude = ('posted_date','company_name','rank')
	
	def __init__(self, *args, **kwargs):
		skills = Skills.objects.all()
		super().__init__(*args, **kwargs)
		self.fields['skills'].widget= forms.SelectMultiple(choices=[(skill.id, skill.name) for skill in skills])
		self.fields['last_date'].widget = forms.DateInput(attrs={'type': 'date'})


class CompanyForm(forms.ModelForm):
	class Meta: 
		model = Company
		fields = '__all__'

class SkillForm(forms.ModelForm):
	class Meta:
		model = Skills
		fields = '__all__'

class StartupForm(forms.ModelForm):
	class Meta:
		model = StartUps
		fields = '__all__'
