import os
from uuid import uuid4
from django.db import models
from autoslug import AutoSlugField
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from django.utils.timezone import now
from mptt.models import MPTTModel, TreeForeignKey
User = settings.AUTH_USER_MODEL

def path_and_rename(instance, filename):
    upload_to = 'file/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class HustleQuerySet(models.QuerySet):
    def updated(self):
        now = timezone.now()
        return self.filter(updated_on__lte=now)

    def search(self, query):
        lookup = (Q(hustle_name__icontains=query) |
                  Q(category__name__icontains=query) |
                  Q(content__icontains=query) |
                  Q(user__username__icontains=query) |
                  Q(user__username__icontains='@' + query) |
                  Q(user__first_name__icontains=query) |
                  Q(user__last_name__icontains=query)
                  )
        return self.filter(lookup)


class HustleManager(models.Manager):
    def get_queryset(self):
        now = timezone.now()
        return HustleQuerySet(self.model, using=self._db)

    def updated(self):
        return self.get_queryset().updated()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().updated().search(query)


# Category
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        return reverse('post_by_category', args=[self.slug])

    def __str__(self):
        return self.name


CHOICES = (
    ("True", "True"),
    ("False", "False")
)


class Hustle(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE, related_name='user')
    hustle_name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='hustle_name',  max_length=200, unique=True, editable=True)
    updated_on = models.DateTimeField(default=now)
    content = models.TextField(max_length=200, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    likes = models.ManyToManyField(User, related_name="hustle_posts")
    category = models.ForeignKey(Category, default=1, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    travel_availability = models.CharField(
        max_length=20,
        choices=CHOICES,
        default='1'
    )
    objects = HustleManager()

    def get_absolute_url(self):
        return f"details/{self.slug}"

    def get_delete_url(self):
        return f"{self.slug}/delete"

    def get_edit_url(self):
        return f"{self.slug}/edit"

    class Meta:
        verbose_name_plural = 'hustles'
        ordering = ['-updated_on']

    def __str__(self):
        return self.hustle_name


class HustleMedia(models.Model):
    hustle = models.ForeignKey(Hustle, on_delete=models.CASCADE, related_name="media")
    file = models.FileField(upload_to=path_and_rename, null=True, blank=True)

    def __str__(self):
        return self.hustle.hustle_name


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey("self", on_delete=models.CASCADE, null=True, related_name="replies")

    class Meta:
        ordering = ('-timestamp',)
        verbose_name_plural = "skills"

    def __str__(self):
        return self.post


class Comment(MPTTModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hustle = models.ForeignKey(Hustle, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    class MPTTMeta:
        order_insertion_by = ('timestamp',)

    def __str__(self):
        return self.comment[0:13] + "... " + "by " + str(self.user)

