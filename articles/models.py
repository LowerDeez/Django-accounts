from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _
import datetime


# Create your models here.
class Article(models.Model):
    DRAFT = 'D'
    PUBLISHED = 'P'
    STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    )

    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(max_length=5000)
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    create_user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ('-create_date', )

    def __str__(self):
        return self.title



