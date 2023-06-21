from django import forms
from .models import Post, User, Comment, PostSort


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'image',)

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'password':forms.PasswordInput(attrs={'label':'Пароль'})
        }

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password','first_name', 'avatar', 'email')
        widgets = {
            'password':forms.PasswordInput(attrs={'label':'Пароль'})
        }

class SearchForm(forms.Form):
    searchfield = forms.CharField(label='', required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {'body': forms.TextInput(attrs={'label':'', 'placeholder':' '}),}

class WikiForm(forms.Form):
    search = forms.CharField(label='')

class SortForm(forms.ModelForm):
    
    class Meta:
        model = PostSort
        fields = ('items',)