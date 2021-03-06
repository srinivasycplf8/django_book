from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from .models import Customer
from django import forms

class CustomerCreationForm(forms.ModelForm):
	password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Confirm your password",widget=forms.PasswordInput)

	class Meta:
		model = Customer
		fields = ['username','fullname','phone','card','address']

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if len(password1)==1:
			raise forms.ValidationError("Password is very short")
		if  not any( char in "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]" for char in password1):
			raise forms.ValidationError("You need to add special characters")
		if password1 and password2 and password2!=password1:
			raise forms.ValidationError("Password does not match.")
		return password2
	

	def save(self, commit=True):
	    user = super(CustomerCreationForm, self).save(commit=False)
	    user.set_password(self.cleaned_data["password1"])
	    if commit:
	        user.save()
	    return user