from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    cluster = []

    def addCluster(self, clus):
        self.cluster.append(clus)

    def __str__(self):
        return f'{self.user.username} Profile'


class CrawlingQueue(models.Model):  # model to store queue of crawler requests made by users
    userName = models.CharField(max_length=100)
    clusterName = models.CharField(max_length=100)
    depth = models.IntegerField()
    strategy = models.CharField(max_length=100, default="")
    url = models.TextField()  # un-parsed urls as long text

class CrawledQueue(models.Model):
    url = models.TextField()

class Item(models.Model):
    username = models.CharField(max_length=100)
    clustername = models.CharField(max_length=100)
    link = models.CharField(max_length=1000)
    content = models.TextField()
