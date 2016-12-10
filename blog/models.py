from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from redactor.fields import RedactorField
from hitcount.models import HitCount, HitCountMixin

class AuditModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(AuditModel):
    phonenumber = models.IntegerField()
    discription = models.ForeignKey(User)
    image = models.ImageField()


class Entry(AuditModel):
    User = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    content = RedactorField(allow_image_upload=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title


class SubscriberNewsletter(AuditModel):
    email = models.EmailField(max_length=255)

    def __str__(self):
        return self.email
