from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    app_label = 'profile'

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
    app_label = 'crawlingQueue'