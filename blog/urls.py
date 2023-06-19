from django.urls import include, path
from rest_framework.routers import DefaultRouter

from blog.views import UserViewSet, TokenObtainPairView, \
    TokenRefreshView, index, PostViewSet, signin, post_form, error, profile,\
          ttest, register_form, UserUpdateView, UserDeleteView, GetUserPostsView,\
            GetPostCommentsView, wiki#, PostCreateView

from django.conf.urls.static import static
from django.conf import settings

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
    path('ttest/',ttest, name='ttest'),
    # path('<username>/edit/', edit_form, name='edit'),
    path('<pk>/update/', UserUpdateView.as_view(), name='update'),
    path('<pk>/delete/', UserDeleteView.as_view(), name='delete'),
    # path('editor/get/', EditorView.as_view()),
    # path('reader/get/', ReaderView.as_view()),
    # path('post/add/', PostCreateView.as_view()),
    path('<fk>/getuserpost/', GetUserPostsView.as_view({'get':'list'})),
    path('<post>/getpostcomment/', GetPostCommentsView.as_view({'get':'list'})),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)