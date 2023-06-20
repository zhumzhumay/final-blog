from django import forms
from .models import Post, User, Comment, PostSort
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

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
    aiman = forms.CharField(label='')

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


# class EditForm(forms.ModelForm):
    # class Meta:
    #     model = User
    #     fields = ('email',)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_method = 'post'
    #     self.helper.add_input(Submit('submit', 'Save'))