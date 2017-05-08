from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save #выполняет код после сохранения обьекта https://docs.djangoproject.com/en/1.11/ref/signals/#post-save
from django.conf import settings

import hashlib
import os.path
import urllib


class UserProfileManager(models.Manager):
    def get_queryset(self):
        return super(UserProfileManager, self).get_queryset().filter(city='London')

# Create your models here.
class UserProfile(models.Model):
    STUDENT = 1
    TEACHER = 2
    SUPERVISOR = 3
    ROLE_CHOICES = (
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
        (SUPERVISOR, 'Supervisor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, default='', blank=True)
    city = models.CharField(max_length=100, default='', blank=True)
    website = models.URLField(default='', blank=True)
    phone = models.IntegerField(default=0)
    birth_date = models.DateField(blank=True, null=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)

    london = UserProfileManager()
    objects = models.Manager()

    def __str__(self):
        return self.user.username

    def get_picture(self):
        no_picture = 'http://dolodom.com/images/nopic.jpg'
        try:
            filename = settings.MEDIA_ROOT + '/profile_pictures/' + \
                       self.user.username + '.jpg'
            picture_url = settings.MEDIA_URL + 'profile_pictures/' + \
                          self.user.username + '.jpg'
            if os.path.isfile(filename):
                return picture_url
            else:
                gravatar_url = 'http://www.gravatar.com/avatar/{0}?{1}'.format(
                    hashlib.md5(self.user.email.lower()).hexdigest(),
                    urllib.urlencode({'d': no_picture, 's': '256'})
                )
                return gravatar_url

        except Exception:
            return no_picture


def create_profile(sender, **kwargs):  # при создании нового пользователя, создается и его профайл
    if kwargs['created']:  # если пользователь создан
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)



#2й вариант реализации функции создания профайла
"""
...
from django.dispatch import receiver
...

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
"""


class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def remove_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)

    @classmethod
    def who_added_user(cls, user):
        users = []
        for friend in cls.objects.all():
            if user in friend.users.all():  # friend instead of friends
                users.append(friend.current_user)
        return users
