from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    cover_image = models.URLField(max_length=2000)
    description = models.TextField(max_length=1000)
    watchlist = models.ManyToManyField(User, blank="true",related_name="tbr")

    def __str__(self):
        return f"{self.title}by{self.author}"

class Club(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_clubs')
    members = models.ManyToManyField(User, through='ClubMembership',related_name='clubs_joined')
    books = models.ManyToManyField(Book)
    imageUrl = models.URLField(max_length=2000)
    isActive = models.BooleanField(default=True)
    profileUrl = models.URLField(max_length=2000)

    def __str__(self):
        return f"{self.name} club is owned by {self.owner}"

class TBRBook(models.Model):
    book = models.ManyToManyField(Book, related_name='tbr')
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.club.name} TBR: {self.book.title}"

class ReadBook(models.Model):
    book = models.ManyToManyField(Book, related_name='read')
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.club.name} Already Read: {self.book.title}"
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,related_name="usercomment")
    message=models.CharField(max_length=400)

    def __str__(self):
        return f'{self.author} commented'
    
class ClubMembership(models.Model):
    user = models.ForeignKey( User, related_name='usermember', on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} joined {self.club}'

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} messsaged in {self.club.name} at {self.created_at}'


class Forum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} messsaged in {self.book.title} at {self.created_at}'