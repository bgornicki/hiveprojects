from django.db import models
from django.utils.translation import ugettext_lazy as _

from package.models import BaseModel, Project
from django.db.models.query import QuerySet

class UpdatePostQuerySet(QuerySet):
    def latest(self):
        return self.order_by("-publish_date").first()

class UpdatePost(BaseModel):
    publish_date = models.DateTimeField(_("Publish Date"))
    body_text = models.TextField(_("Post Body Text"), blank=True, null=True)
    link = models.CharField(max_length=254, verbose_name='Link', default="")
    title = models.CharField(max_length=254, verbose_name='Title', default="")
    projects = models.ManyToManyField(Project)

    objects = UpdatePostQuerySet.as_manager()

    def save(self, *args, **kwargs):
        super(UpdatePost, self).save(*args, **kwargs)
