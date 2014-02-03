from django.db import models


class TweetMessage(models.Model):
    tweet_id = models.IntegerField()
    text = models.TextField()