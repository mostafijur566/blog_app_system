from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils.timezone import datetime


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("users must have an email address")
        if not username:
            raise ValueError("users must have a username")
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Account(AbstractBaseUser):
    name = models.CharField(max_length=60)
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True, primary_key=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Category(models.Model):
    name = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=False, blank=False)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, default='Other')
    title = models.CharField(max_length=200)
    body = models.TextField()
    post_date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-post_date']


class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, null=False, blank=False)
    comment = models.TextField()
    comment_date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.comment[0:50]
