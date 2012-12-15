from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class RoomCategory(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=512)
    is_private = models.BooleanField()
    created_by = models.ForeignKey(User)
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(RoomCategory)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Room, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('room_detail', (), {
            'slug': self.slug,
            'pk': self.id,
        })
