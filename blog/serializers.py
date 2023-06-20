from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Post, Comment, LikeDislike


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'role', 'id', 'password']


class TokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, *args, **kwargs):
        data = super().validate(*args, **kwargs)

        if not self.user.is_active:
            raise AuthenticationFailed({
                'detail': f"Пользователь {self.user.username} был деактивирован!"
            }, code='user_deleted')

        data['id'] = self.user.id
        data['username'] = self.user.username

        return data


class TokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])

        try:
            user = User.objects.get(
                pk=refresh.payload.get('user_id')
            )
        except ObjectDoesNotExist:
            raise serializers.ValidationError({
                'detail': f"Пользователь был удалён!"
            }, code='user_does_not_exists')

        if user.blocked:
            raise AuthenticationFailed({
                'detail': f"Пользователь {user.username} был заблокирован!"
            }, code='user_deleted')

        data['id'] = user.id
        data['username'] = user.username

        return data


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
    # def get_post(self, obj):
    #     serializer = GetUserSerializer(obj.postde)
    #     return serializer.data


class PostSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    # type_name = serializers.SerializerMethodField()
    date_time = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_user_info(self, obj):
        serializer = GetUserSerializer(obj.user)
        return serializer.data

    # def get_type_name(self, obj):
    #     return Post.NEWS_TYPES[int(obj.type) - 1][1]

    def get_date_time(self, obj):
        return obj.date_post.strftime("%d/%m/%Y, %H:%M")
    
class LikeDisLikeSerializer(serializers.ModelSerializer):
    # user_info = serializers.SerializerMethodField()
    # post_info = serializers.SerializerMethodField()

    class Meta:
        model = LikeDislike
        fields = '__all__'


  

class PostCommentsSerializer(serializers.ModelSerializer):
    # user_id = serializers.SerializerMethodField()
    user_info = serializers.SerializerMethodField()
    date_time = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = '__all__'
    
    def get_date_time(self, obj):
        return obj.date_comment.strftime("%d/%m/%Y, %H:%M")
    
    def get_user_info(self, obj):
        serializer = GetUserSerializer(obj.author)
        return serializer.data


