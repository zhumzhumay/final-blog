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
from blog.models import User, Post, Comment
# from blog.permissions import IsSuperAdmin, IsReader
from blog.serializers import UserSerializer, TokenObtainPairSerializer, TokenRefreshSerializer, PostSerializer,\
GetUserPostsSerializer, GetPostCommentsSerializer

from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
import geoip2.database, wikipediaapi



class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class GetUserPostsView(GenericViewSet ,mixins.ListModelMixin):
    serializer_class = GetUserPostsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        
        user = self.kwargs['fk']
        return Post.objects.filter(user=user)
    
class GetPostCommentsView(GenericViewSet ,mixins.ListModelMixin):
    serializer_class = GetPostCommentsSerializer
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


# class PostViewSet (mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
#                    GenericViewSet):
class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    queryset = Post.objects.all().order_by('-date_post')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'text', 'user__username', 'user__first_name'] #user_info.username
    ordering_fields = ['date_post']

    # def get_queryset(self):
        
    #     ord = self.kwargs['order']
    #     return Post.objects.all().order_by(ord)

class UserUpdateView(UpdateView):
    model = User
    fields = ['first_name', 'email','avatar', 'description']
    success_url = reverse_lazy('index')

class UserDeleteView(DeleteView):
    model = User
    fields = ['first_name', 'email','avatar']
    success_url = reverse_lazy('index')


# class PostCreateView(mixins.CreateModelMixin, GenericViewSet):
#     permission_classes = [IsEditor | IsSuperAdmin]
#     def get(self, request, *args, **kwargs):
#         return Response(data={'success': 'You posted it'}, status=status.HTTP_200_OK)

def index(request):
    # submitbutton= request.POST.get("submit")
    sortform = SortForm(request.GET or None)
    form = SearchForm(request.POST or None)
    sort = '-date_post'
    if sortform.is_valid():
        sort = sortform.cleaned_data.get('items')
    if form.is_valid():
        aiman = form.cleaned_data.get("aiman")
       
        return render(request, 'index.html',{'form':form, 'aiman':aiman, 'sortform':sortform})
        
    return render(request, 'index.html',{'form':form, 'sort':sort, 'sortform':sortform})
        
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
            return redirect('index')
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
        # return render(request, 'profile.html', {'username':username, 'country':country, 'city':city, 'form':form})   
    else:
        form = CommentForm(initial={'body':None})


    return render(request, 'profile.html', {'username':username, 'country':country, 'city':city, 'form':form})

def ttest(request):
    return render(request, 'ttest.html')

# def login_form(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             # post = form.save(commit=False)
#             # if Sessions.objects.get(id=User.objects.get(username=post.username).id):
#             #     Sessions.objects.get(id=User.objects.get(username=post.username).id).delete()
#             # post.date = timezone.now()
#             # post.token =
#             # post.save()
#             return redirect('index')
#     else:
#         form = LoginForm()
#     return render(request, 'signin.html', {'form': form})
