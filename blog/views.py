import json
from django.views import View
import django_filters.rest_framework
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from rest_framework import status, mixins, filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.views.generic import CreateView, UpdateView, DeleteView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.views import TokenObtainSlidingView, TokenRefreshSlidingView

from blog.forms import PostForm, LoginForm, RegisterForm, SearchForm, CommentForm, WikiForm, SortForm
from blog.models import User, Post, Comment, LikeDislike
# from blog.permissions import IsSuperAdmin, IsReader
from blog.serializers import UserSerializer, TokenObtainPairSerializer, TokenRefreshSerializer, PostSerializer,\
PostCommentsSerializer, LikeDisLikeSerializer

from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
import geoip2.database, wikipediaapi
from django.contrib.contenttypes.models import ContentType




class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class GetUserPostsView(GenericViewSet ,mixins.ListModelMixin):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        
        user = self.kwargs['fk']
        return Post.objects.filter(user=user).order_by('-date_post')
    
class GetPostCommentsView(GenericViewSet ,mixins.ListModelMixin):
    serializer_class = PostCommentsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        
        post = Post.objects.get(id=self.kwargs['post'])
        return Comment.objects.filter(post=post)

class TokenObtainPairView(TokenObtainSlidingView):
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairSerializer


class TokenRefreshView(TokenRefreshSlidingView):
    permission_classes = [AllowAny]
    serializer_class = TokenRefreshSerializer


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    queryset = Post.objects.all().order_by('-date_post')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'text', 'user__username', 'user__first_name'] #user_info.username
    ordering_fields = ['date_post']


class LikeDisLikeViewSet(ModelViewSet):
    serializer_class = LikeDisLikeSerializer
    permission_classes = [AllowAny]
    queryset = LikeDislike.objects.all()
    
class GetLikeDisLikeView(GenericViewSet ,mixins.ListModelMixin):
    serializer_class = LikeDisLikeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        
        user = self.kwargs['userpk']
        post = self.kwargs['postpk']
        queryset = LikeDislike.objects.filter(user=user, post=post)
        # if queryset.count()==0:
        #     return Null
        # else:
        #     return queryset
        return queryset


    


class UserUpdateView(UpdateView):
    model = User
    fields = ['first_name', 'email','avatar', 'description']
    success_url = reverse_lazy('index')

class UserDeleteView(DeleteView):
    model = User
    fields = ['first_name', 'email','avatar']
    success_url = reverse_lazy('index')


def index(request):
    # submitbutton= request.POST.get("submit")
    sortform = SortForm(request.GET or None)
    form = SearchForm(request.POST or None)
    sort = '-date_post'
    aiman = ''
    if sortform.is_valid():
        sort = sortform.cleaned_data.get('items')
    if form.is_valid():
        aiman = form.cleaned_data.get("aiman")
       
        
    return render(request, 'index.html',{'form':form, 'sort':sort, 'sortform':sortform, 'aiman':aiman,})
        
def wiki(request):
    submitbutton= request.POST.get("submit")
    form = WikiForm(request.POST or None)

    wiki_wiki = wikipediaapi.Wikipedia(language='ru',
        extract_format=wikipediaapi.ExtractFormat.HTML)
    wiki_text = wikipediaapi.Wikipedia('ru')
    full = 'https://ru.wikipedia.org/wiki/'
    if form.is_valid():
        search = form.cleaned_data.get('search')
        page_txt = wiki_text.page(search)
        page_ru = wiki_wiki.page(search)
        
        if page_txt.exists()==True:
            page = page_ru.text
            full = page_ru.fullurl

        else:
            page = 'Такой статьи не существует'
            
       
        return render(request, 'wiki.html',{'form':form, 'page':page, 'full':full,'submitbutton': submitbutton})
    return render(request, 'wiki.html',{'form':form, 'submitbutton': submitbutton, 'full':full})


def error(request):
    return render(request, 'error.html')


def signin(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # if user.role == User.ROLE_TYPES[0][0]:
            return redirect('profile', user.username)
            # else:
            #     return redirect('index')
        else:
            # Return an 'invalid login' error message.
            return redirect('error')
    else:
        form = LoginForm()

        # Redirect to a success page.

    return render(request, 'signin.html', {'form': form})


def post_form(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.post_date = timezone.now()
            post.save()
            # img_obj = form.instance
            return redirect('profile', request.user.username)
    else:
        form = PostForm()
    return render(request, 'post_add.html', {'form': form})

def register_form(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('signin')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})




def profile(request, username):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    with geoip2.database.Reader('geoip/GeoLite2-City.mmdb') as reader:
        response = reader.city('5.34.91.6')
    country = response.country.names['ru']
    city = response.city.names['ru']

    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.comment_date = timezone.now()
            post = request.POST.get('post_id')
            comment.post=Post.objects.get(id=post)
            comment.save()
        return HttpResponseRedirect(request.path) 
    else:
        form = CommentForm(initial={'body':None})


    return render(request, 'profile.html', {'username':username, 'country':country, 'city':city, 'form':form})

# def ttest(request):
#     return render(request, 'ttest.html')


def single_post(request,title, pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.comment_date = timezone.now()
            post = request.POST.get('post_id')
            comment.post=Post.objects.get(id=post)
            comment.save()
        return HttpResponseRedirect(request.path) 
    else:
        form = CommentForm(initial={'body':None})
    return render(request, 'single_post.html', {'title':title, 'pk':pk, 'form':form})

# class VotesView(View):
#     model = None    # Модель данных - Статьи или Комментарии
#     vote_type = None # Тип комментария Like/Dislike
 
#     def post(self, request, pk):
#         obj = self.model.objects.get(pk=pk)
#         # GenericForeignKey не поддерживает метод get_or_create
#         try:
#             likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, user=request.user)
#             if likedislike.vote is not self.vote_type:
#                 likedislike.vote = self.vote_type
#                 likedislike.save(update_fields=['vote'])
#                 result = True
#             else:
#                 likedislike.delete()
#                 result = False
#         except LikeDislike.DoesNotExist:
#             obj.votes.create(user=request.user, vote=self.vote_type)
#             result = True
 
#         return HttpResponse(
#             json.dumps({
#                 "result": result,
#                 "like_count": obj.votes.likes().count(),
#                 "dislike_count": obj.votes.dislikes().count(),
#                 "sum_rating": obj.votes.sum_rating()
#             }),
#             content_type="application/json"
#         )