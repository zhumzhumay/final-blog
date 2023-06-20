from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.db.models import Sum

class UserManager(BaseUserManager):

    def create_user(self, username, password=None):
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        user.role = 1
        return user
    

 
 
# class LikeDislikeManager(models.Manager):
#     use_for_related_fields = True
 
#     def likes(self):
#         # Забираем queryset с записями больше 0
#         return self.get_queryset().filter(vote__gt=0)
 
#     def dislikes(self):
#         # Забираем queryset с записями меньше 0
#         return self.get_queryset().filter(vote__lt=0)
 
#     def sum_rating(self):
#         # Забираем суммарный рейтинг
#         return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0