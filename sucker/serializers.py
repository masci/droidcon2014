from rest_framework import serializers

from .models import TweetMessage


class TweetMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetMessage
        fields = ('tweet_id', 'text')
