from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField()

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Tag(models.Model):
    caption = models.CharField(max_length=50)

    def __str__(self):
        return self.caption

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    is_manager =models.BooleanField(default=False)
    def __str__(self):
        return str(self.user)


class Post(models.Model):
    #name=models.ForeignKey(User,on_delete=models.CASCADE,default='1')
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=300)
    image = models.CharField(max_length=100)
    date= models.DateTimeField()
    content = models.TextField(validators=[MinLengthValidator(50)])
    slug = models.SlugField(db_index=True, unique=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="posts")
    tags = models.ManyToManyField(Tag)
    category=models.CharField(max_length=100,default='fun')
    venue=models.CharField(max_length=100,default="none")
    total_seats=models.IntegerField(default=10)

    def __str__(self):
        return self.title





class RegisterEvent(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    seats = models.IntegerField(default=1)
    # text = models.TextField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="registrations")




