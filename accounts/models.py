from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, User, BaseUserManager


class UserManager(BaseUserManager):

    def create(self, password, **kwargs):
        instance = self.model(**kwargs)
        instance.set_password(password)
        instance.save()
        return instance

    def create_user(self, **kwargs):
        return self.create(**kwargs)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractBaseUser):

    email = models.EmailField(unique=True, blank=False, null=False)
    date_joined = models.DateField(verbose_name='registration date',
                                   auto_now_add=True, editable=False)
    is_staff = models.BooleanField(default=False, null=False, blank=False)
    first_name = models.CharField(null=False, blank=True, max_length=100)
    last_name = models.CharField(null=False, blank=True, max_length=100)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return str(self.pk) + '. ' + str(self.email)


@receiver(pre_delete, sender=User)
def clear_related_likes(instance, **kwargs):
    instance.likes.all().delete()


@receiver(pre_delete, sender=User)
def clear_related_posts(instance, **kwargs):
    instance.posts.all().delete()
