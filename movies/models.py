from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify


class Comment(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.movie.name}'


class Rating(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.movie.name} - {self.value}'


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering=('name',)
        verbose_name='category'
        verbose_name_plural='categories'

    def get_url(self):
        return reverse('movies:movies_by_category', args=[self.slug])

    def __str__(self):
        return '{}'.format(self.name)


class Movie(models.Model):
    name=models.CharField(max_length=250, unique=True)
    slug=models.SlugField(max_length=250, unique=True)
    description=models.TextField(blank=True)
    release_date=models.DateField()
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='product', blank=True)
    actors=models.CharField(max_length=1000)
    trailer_link=models.CharField(max_length=500)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    ratings = models.ManyToManyField('Rating', related_name='movies')
    comments = models.ManyToManyField('Comment', related_name='movies')

    def get_url(self):
        return reverse('movies:movies_category_detail', args=[self.category.slug, self.slug])

    class Meta:
        ordering=('name',)
        verbose_name='movie'
        verbose_name_plural='movies'

    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
