from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import  Post, RegisterEvent
from django import forms


class RegisterEventForm(ModelForm):
    class Meta:
        model = RegisterEvent
        exclude = ["post"]
        labels = {"user_name": "Your Name",
                  "user_email": "Your email","seats":"no of Seats"}


class UploadForm(ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
class UpdateEventForm(forms.ModelForm):
    class Meta:
        model=Post
        fields="__all__"
    def save(self,commit=True):
        post=self.instance
        post.title=self.cleaned_data['title']
        post.summary=self.cleaned_data['summary']
        if commit:
            post.save()
        return post

#registeration form
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data ['email']
        if commit:
            user.save()
        return user
