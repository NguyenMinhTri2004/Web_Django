from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import django.contrib.postgres.fields
from django.contrib.auth.forms import UserCreationForm
from django.forms import FloatField
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email', 'password1' , 'password2')
    
class Status(models.Model):
    id = models.CharField(max_length=200, null=False , blank=True , primary_key=True,  unique=True)
    name = models.CharField(max_length=200, blank=True)  
    
    def __str__(self) :
        return self.name
class Author(models.Model):
    id = models.CharField(max_length=200, null=False , blank=True , primary_key=True,  unique=True)
    name = models.CharField(max_length=200, blank=True)  
    
    def __str__(self) :
        return self.name
 
 
class Category(models.Model):
    id = models.CharField(max_length=200, null=False , blank=True , primary_key=True,  unique=True)
    name = models.CharField(max_length=200 , blank=True)
    
    def __str__(self) :
        return self.name
 
    
    
class Manga(models.Model):
    idManga = models.CharField(max_length=200, null=False , blank=True , primary_key=True,  unique=True)
    name = models.CharField(max_length=200, null=True , blank=True)
    description = models.CharField(max_length=200, null=True , blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, to_field='id')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, to_field='id')
    category = models.ForeignKey(Category, on_delete=models.CASCADE , to_field='id')
    viewCount = models.IntegerField(null=True, blank=True)
    likedList =ArrayField(
        models.CharField(max_length=200, blank=True , null=True),
        size=20
    )
    image = models.ImageField(null=True, blank=True)
    # comment = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self) :
        return self.idManga
    
class Chapter(models.Model):
    idChapter = models.ForeignKey(Manga, on_delete=models.CASCADE, to_field='idManga')
    name = models.CharField(max_length=200, null=True , blank=True)
    viewCount = models.IntegerField(null=True, blank=True)
    # updateAt = models.CharField(max_length=200, null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    # comment = ArrayField(models.CharField(max_length=200), blank=True)
    content = ArrayField(
        models.CharField(max_length=200, blank=True),
        size=20
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self) :
        return self.name
    
class Myrating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])

class MyList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    watch = models.BooleanField(default=False)
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    context = models.CharField(max_length=200 , null=True , blank=True)
    
class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.CharField(max_length=200 , null=True , blank=True)
    
