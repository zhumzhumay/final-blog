from django.urls import include, path
from rest_framework.routers import DefaultRouter

from blog.views import UserViewSet, TokenObtainPairView, \
    TokenRefreshView, index, PostViewSet, signin, post_form, error, profile,\
          register_form, UserUpdateView, UserDeleteView, GetUserPostsView,\
            GetPostCommentsView, wiki, single_post#, PostCreateView

from django.conf.urls.static import static
from django.conf import settings
from .models import Comment


router = DefaultRouter()
router.register('user', UserViewSet, basename="user")
router.register('post', PostViewSet, basename='post')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', index, name='index'),
    path('wiki/', wiki, name='wiki'),
    path('post/new/', post_form, name='post_add'),
    path('error/', error, name='error'),
    path('signin/', signin, name='signin'),
    path('register/', register_form, name='register'),
    path('<username>/profile/',profile, name='profile'),
    # path('ttest/',ttest, name='ttest'),
    path('single_post/<pk>/<title>', single_post, name='single_post'),
    path('<pk>/update/', UserUpdateView.as_view(), name='update'),
    path('<pk>/delete/', UserDeleteView.as_view(), name='delete'),
    path('<fk>/getuserpost/', GetUserPostsView.as_view({'get':'list'})),
    path('<post>/getpostcomment/', GetPostCommentsView.as_view({'get':'list'})),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),




    # path(r'^article/(?P<pk>\d+)/like/$',
    #     VotesView.as_view(model=Comment, vote_type=LikeDislike.LIKE),
    #     name='article_like'),
    # path(r'^article/(?P<pk>\d+)/dislike/$',VotesView.as_view(model=Comment, vote_type=LikeDislike.DISLIKE),
    #     name='article_dislike'),
    # path(r'^comment/(?P<pk>\d+)/like/$',VotesView.as_view(model=Comment, vote_type=LikeDislike.LIKE),
    #     name='comment_like'),
    # path(r'^comment/(?P<pk>\d+)/dislike/$',VotesView.as_view(model=Comment, vote_type=LikeDislike.DISLIKE),
    #     name='comment_dislike'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)