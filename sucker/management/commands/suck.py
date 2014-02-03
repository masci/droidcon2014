from django.core.management.base import BaseCommand, CommandError

import json

from ...models import TweetMessage
from ...twittersucker import TwitterStream


class TwitterSucker(TwitterStream):
    """
    Custom version of the TwitterStream, save messages into database
    """
    def handle_tweet(self, data):
        """ This method is called when data is received through Streaming endpoint.
        """
        self.buffer += data
        if data.endswith('\r\n') and self.buffer.strip():
            # complete message received
            message = json.loads(self.buffer)
            self.buffer = ''
            if message.get('limit'):
                self.stderr.write('Rate limiting caused us to miss %s tweets' % (message['limit'].get('track')))
            elif message.get('disconnect'):
                raise Exception('Got disconnect: %s' % message['disconnect'].get('reason'))
            elif message.get('warning'):
                self.stderr.write('Got warning: %s' % message['warning'].get('message'))
            else:
                TweetMessage.objects.create(tweet_id=message.get('id'), text=message.get('text'))


class Command(BaseCommand):
    help = 'Suck tweets from stream'

    def handle(self, *args, **options):
        ts = TwitterSucker()
        ts.setup_connection()
        ts.start()