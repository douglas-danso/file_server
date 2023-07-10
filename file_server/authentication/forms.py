from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
# from django.contrib.auth.forms import PasswordResetForm
from .validator import CustomPasswordValidator

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    

    class Meta:
        model = CustomUser
        fields = ['email']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('Passwords do not match')
            
        validator = CustomPasswordValidator()
        validator.validate(password)
        
        return password
    

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.is_active = False
            user.save()
        return user

class CustomPasswordResetForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = []
    password1 = forms.CharField(
        label= 'new password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        
    )

    password2 = forms.CharField(
        label= 'new password confirmation',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

  

    def clean(self):
        cleaned_data = super().clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
            
        validator = CustomPasswordValidator()
        validator.validate(password1)
        
        return cleaned_data

    def save(self, commit=True):
        new_password = super(CustomPasswordResetForm, self).save(commit=False)
        new_password.set_password(self.cleaned_data['password1'])
        if commit:
            new_password.save()
        return new_password
    



class LogInForm(AuthenticationForm):
    pass
