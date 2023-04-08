from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from ckeditor.fields import RichTextField
from django.db.models.base import Model
from django.db.models.signals import pre_save
from .utils import unique_slug_generator,category_slug_generator
from django.urls import reverse




# Create your models here.
class PostComment(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f'{self.sender.get_username()}'

class Categories(models.Model):
    categoryname = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.categoryname

def slug_generator_category(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = category_slug_generator(instance)
pre_save.connect(slug_generator_category, sender=Categories)

class Post(models.Model):
    title = models.CharField(max_length=255)
    title_tag = models.CharField(max_length=255, default='Blog Post')
    slug = models.SlugField(max_length=255, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='blog', null=True, blank=True)
    body = RichTextField(blank=False, null=True)
    comments = models.ManyToManyField(PostComment, blank=True)
    post_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Categories, null=True, on_delete=models.PROTECT, related_name='category_set')
    meta_title=models.CharField(max_length=255, null=True, blank=True)
    meta_description=models.TextField(max_length=3000,null=True, blank=True)
    image_alt=models.CharField(max_length=1500,blank=True,null=True)

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        return reverse('blog-detail',kwargs={'slug':self.slug})

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Post)
