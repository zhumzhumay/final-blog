from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from blog.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    SUPERADMIN, READER = range(1, 3)
    ROLE_TYPES = (
        (SUPERADMIN, 'Суперпользователь'),
        (READER, 'Читатель')
    )

    objects = UserManager()

    id = models.AutoField(primary_key=True)
    username = models.CharField('Логин', max_length=50, default='', unique=True)
    first_name = models.CharField("ФИО", max_length=100, default='', blank=True, null=True)
    avatar = models.ImageField('Аватарка', default='ava-default.png')
    email = models.EmailField("Почта", default="email@mail.com", blank=True, null=True)
    description = models.TextField('Обо мне', default='')
    date_joined = models.DateTimeField("Дата присоединения", blank=True, null=True, default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(
        default=True,
        verbose_name='Статус доступа',
    )
    role = models.IntegerField('Роль', default=READER, choices=ROLE_TYPES)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        # Если пароль не хэширован, то хэшируем его перед сохранением
        if not self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_absolute_image_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return ''




class Post(models.Model):
    # URGENT, BESTOFTHEDAY, REGULAR = range(1, 4)
    # NEWS_TYPES = (
    #     (URGENT, 'СРОЧНАЯ НОВОСТЬ'),
    #     (BESTOFTHEDAY, 'НОВОСТЬ ДНЯ'),
    #     (REGULAR, 'ОБЫЧНАЯ')
    # )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='posts',
                             default=0)
    
    image = models.ImageField('Изображение', default='static/img/service-6.jpg')
    title = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name='Заголовок')
    text = models.TextField(verbose_name="Текст", default='')
    date_post = models.DateTimeField(default=timezone.now, verbose_name="Дата")
    
    # votes = GenericRelation(LikeDislike, related_query_name='comments')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    def get_absolute_image_url(self):
        if self.image:
            return self.image.url
        else:
            return ''

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост', related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='comments')
    body = models.TextField('Комментарий', max_length=255)
    date_comment = models.DateTimeField(default=timezone.now, verbose_name="Дата")
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.post.title

class PostSort(models.Model):
    CHOICES = (
        ('date_post','сначала старые посты'),
        ('-date_post', 'сначала новые посты')
    )


    items = models.CharField('Сортировать', choices=CHOICES, default='-date_post', max_length=100)

class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1
 
    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )
    
    post = models.ForeignKey(Post, verbose_name="Пост", on_delete=models.CASCADE, default=0, related_name='likes')
    vote = models.SmallIntegerField(verbose_name="Голос", choices=VOTES)
    
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, default=0, related_name='likes')
    
 
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey()
 
#     objects = LikeDislikeManager()

