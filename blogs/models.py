from django.db import models
from django.utils.text import slugify
from accounts.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['-created_at']
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# class Post(models.Model):
#     # Post status
#     PUBLISH_STATUS_CHOICES = [
#         ('draft', 'Draft'),
#         ('published', 'Published'),
#         ('archived', 'Archived'),
#     ]

#     # Content-related fields
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     slug = models.SlugField(unique=True, null=True, blank=True)
#     featured_image = models.ImageField(upload_to='featured_images/', null=True, blank=True)
#     tags = models.ManyToManyField(Tag, blank=True)

#     # User and approval-related fields
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     is_approved = models.BooleanField(default=False)

#     # Post visibility and timing
#     status = models.CharField(max_length=10, choices=PUBLISH_STATUS_CHOICES, default='draft')
#     publish_date = models.DateTimeField(null=True, blank=True)
#     expiry_date = models.DateTimeField(null=True, blank=True)

#     # Additional post metadata
#     view_count = models.IntegerField(default=0)
#     comment_count = models.IntegerField(default=0)
#     post_type = models.CharField(max_length=50, choices=[('article', 'Article'), ('news', 'News'), ('event', 'Event')], default='article')
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

#     # Timestamps
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     # String representation
#     def __str__(self):
#         return self.title

#     # Save method to handle slug generation and publish_date
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.title)
        
#         # Automatically set the publish_date when the post is published
#         if self.status == 'published' and not self.publish_date:
#             self.publish_date = self.updated_at  # Set to the current time
        
#         super().save(*args, **kwargs)

#     # Meta options for ordering and verbose names
#     class Meta:
#         ordering = ['-created_at']
#         verbose_name = 'Post'
#         verbose_name_plural = 'Posts'


# # Pre-save signal to handle unique slugs more effectively
# @receiver(pre_save, sender=Post)
# def ensure_unique_slug(sender, instance, **kwargs):
#     if not instance.slug:
#         instance.slug = slugify(instance.title)
    
#     # Ensure unique slug
#     if Post.objects.filter(slug=instance.slug).exists():
#         instance.slug = f"{instance.slug}-{instance.id}"


