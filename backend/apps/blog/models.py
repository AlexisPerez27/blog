import uuid

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify

from ckeditor.fields import RichTextField

from .utils import get_client_ip

def blog_images_directory(instancia, filename):
    return "blog/{0}/{1}".format(instancia.titulo, filename)

def categoria_images_directory(instancia, filename):
    return "categoria/{0}/{1}".format(instancia.nombre,filename)

# Create your models here.

class Categoria(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    parent = models.ForeignKey("self", related_name="children",on_delete=models.CASCADE, blank=True, null=True)

    nombre = models.CharField(max_length=255)
    titulo = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    imagenes = models.ImageField(upload_to=categoria_images_directory, blank=True, null=True)
    slug = models.CharField(max_length=128)

    def __str__(self):
        return self.nombre



class Post(models.Model):

    class postobject(models.Manager): 
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    status_option = (
        ("draft", "Draft"),
        ("published", "Published")
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    titulo = models.CharField(max_length=128)
    descripcion = models.CharField(max_length=256)
    # contenido = models.TextField()
    contenido = RichTextField(blank=True, null=True)
    imagenes = models.ImageField(upload_to=blog_images_directory)

    keywords = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    views = models.IntegerField(default=0)


    status = models.CharField(max_length=10, choices=status_option, default='draft')

    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    objects = models.Manager()
    postobject = postobject()


    class Meta: 
        ordering = ("status","-created_at")

    def __str__(self):
        return self.titulo
    


class PostView(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postview')
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now=True)



class PostAnalytics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_analytics')
    views = models.PositiveIntegerField(default=0)
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    click_through_rate = models.FloatField(default=0)
    avg_time_on_page = models.FloatField(default=0)


    def increment_click(self):
        self.clicks +=1
        self.save()
        self._update_click_through_rate()

    def _update_click_through_rate(self):
        if self.impressions > 0:
            self.click_through_rate = (self.clicks/self.impressions) * 100
        else: 
            self.click_through_rate = 0
        self.save()

    def increment_impression(self):
        self.impressions +=1
        self.save()
        self._update_click_through_rate()


    def increment_view(self, ip_add): #request
        # ip_add = get_client_ip(request)

        if not PostView.objects.filter(post=self.post, ip_address = ip_add).exists():
            PostView.objects.create(post=self.post, ip_address = ip_add)

            self.views +=1
            self.save()

        
class Heading(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='headings')

    titulo = models.CharField(max_length=255)

    slug = models.CharField(max_length=255)
    level = models.IntegerField(
        choices=(
            (1,"h1"),
            (2,"h2"),
            (3,"h3"),
            (4,"h4"),
            (5,"h5"),
            (6,"h6"),
        )
    )
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def save(self, *args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args,**kwargs)



@receiver(post_save, sender=Post)

def create_post_analytics(sender,instance, created, **kwargs):
    if created:
        PostAnalytics.objects.create(post = instance)