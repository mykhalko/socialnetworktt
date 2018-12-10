from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class Post(models.Model):

    title = models.CharField(null=False, blank=False, max_length=255)
    text = models.TextField(null=False, blank=True)
    author = models.ForeignKey('accounts.User', null=False, blank=False,
                               on_delete=models.CASCADE, related_name='posts')
    likes = models.ManyToManyField('accounts.User', blank=True, related_name='likes')

    def __str__(self):
        return str(self.pk) + '. ' + str(self.title)


@receiver(pre_delete, sender=Post)
def clear_related_likes(instance, **kwargs):
    instance.likes.all().delete()
