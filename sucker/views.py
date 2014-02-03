from rest_framework import viewsets, filters

from .models import TweetMessage
from .serializers import TweetMessageSerializer


class TweetViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TweetMessageSerializer

    def get_queryset(self):
        qs = TweetMessage.objects.all()

        tweet_id = self.request.QUERY_PARAMS.get('id', None)
        if tweet_id is not None:
            qs = qs.filter(tweet_id__gt=tweet_id)

        return qs.order_by('-tweet_id')