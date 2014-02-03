sample = r"""
{"created_at":"Sun Feb 02 21:41:11 +0000 2014","id":430093567592517632,"id_str":"430093567592517632","text":"@DroidRover go beyond","source":"\u003ca href=\"https:\/\/about.twitter.com\/products\/tweetdeck\" rel=\"nofollow\"\u003eTweetDeck\u003c\/a\u003e","truncated":false,"in_reply_to_status_id":null,"in_reply_to_status_id_str":null,"in_reply_to_user_id":2323779140,"in_reply_to_user_id_str":"2323779140","in_reply_to_screen_name":"DroidRover","user":{"id":25575225,"id_str":"25575225","name":"Massimiliano Pippi","screen_name":"maxpippi","location":"","url":"http:\/\/dev.pippi.im","description":"Software developer, Python lover, Dad.","protected":false,"followers_count":202,"friends_count":176,"listed_count":9,"created_at":"Fri Mar 20 21:00:09 +0000 2009","favourites_count":35,"utc_offset":3600,"time_zone":"Rome","geo_enabled":true,"verified":false,"statuses_count":880,"lang":"en","contributors_enabled":false,"is_translator":false,"is_translation_enabled":false,"profile_background_color":"022330","profile_background_image_url":"http:\/\/abs.twimg.com\/images\/themes\/theme1\/bg.png","profile_background_image_url_https":"https:\/\/abs.twimg.com\/images\/themes\/theme1\/bg.png","profile_background_tile":false,"profile_image_url":"http:\/\/pbs.twimg.com\/profile_images\/1504701775\/32_normal.jpg","profile_image_url_https":"https:\/\/pbs.twimg.com\/profile_images\/1504701775\/32_normal.jpg","profile_link_color":"0084B4","profile_sidebar_border_color":"A8C7F7","profile_sidebar_fill_color":"C0DFEC","profile_text_color":"333333","profile_use_background_image":false,"default_profile":false,"default_profile_image":false,"following":null,"follow_request_sent":null,"notifications":null},"geo":null,"coordinates":null,"place":null,"contributors":null,"retweet_count":0,"favorite_count":0,"entities":{"hashtags":[],"symbols":[],"urls":[],"user_mentions":[{"screen_name":"DroidRover","name":"DroidRover","id":2323779140,"id_str":"2323779140","indices":[0,11]}]},"favorited":false,"retweeted":false,"filter_level":"medium","lang":"en"}
"""

curl = """curl --request 'POST' 'https://stream.twitter.com/1.1/statuses/filter.json' --data 'track=droidrover' --header 'Authorization: OAuth oauth_consumer_key="qPFIo42gtwh9whOcWjZr6Q", oauth_nonce="136046c24893b4a6d9d09ce848fb1f70", oauth_signature="ygwUwmaaOeYPpIC8plenlbJ3phg%3D", oauth_signature_method="HMAC-SHA1", oauth_timestamp="1391387749", oauth_token="902555947-W9R96KP9MKNoVekzpc1t9a2W1SpvwCT5rZZIICcb", oauth_version="1.0"' --verbose"""
curl += ' --silent --trace-ascii -'

import json
import subprocess
import sys
"""
if __name__ == '__main__':

    test_cmd = ['./simulate']
    p = subprocess.Popen(curl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, close_fds=True)
    while True:
        sys.stdout.flush()

        line = p.stdout.readline()
        print line
        
        try:
            data = json.loads(line)
            print '--->', data['text'], data['id']
        except ValueError:
            pass

        if line == '' and p.poll() != None:
            break
"""

#!/usr/bin/python
# -*- coding: utf-8 -*-
    
import time
import pycurl
import urllib
import json
import oauth2 as oauth

API_ENDPOINT_URL = 'https://stream.twitter.com/1.1/statuses/filter.json'
USER_AGENT = 'TwitterStream 1.0' # This can be anything really

# You need to replace these with your own values
OAUTH_KEYS = {'consumer_key': 'qPFIo42gtwh9whOcWjZr6Q',
              'consumer_secret': 'amsDiumeMdXOC6oRahc6PBh7ebsEEzky6VbCMR2XIQ',
              'access_token_key': '902555947-W9R96KP9MKNoVekzpc1t9a2W1SpvwCT5rZZIICcb',
              'access_token_secret': '747fZBxqOErvvgN9WtHKsv1WYe0royE8iWGVhBiOuovaS'}

# These values are posted when setting up the connection
POST_PARAMS = {'include_entities': 0,
               'stall_warning': 'true',
               'track': 'droidrover'}


class TwitterStream:
    def __init__(self, timeout=False):
        self.oauth_token = oauth.Token(key=OAUTH_KEYS['access_token_key'], secret=OAUTH_KEYS['access_token_secret'])
        self.oauth_consumer = oauth.Consumer(key=OAUTH_KEYS['consumer_key'], secret=OAUTH_KEYS['consumer_secret'])
        self.conn = None
        self.buffer = ''
        self.timeout = timeout
        self.setup_connection()

    def setup_connection(self):
        """ Create persistant HTTP connection to Streaming API endpoint using cURL.
        """
        if self.conn:
            self.conn.close()
            self.buffer = ''
        self.conn = pycurl.Curl()
        # Restart connection if less than 1 byte/s is received during "timeout" seconds
        if isinstance(self.timeout, int):
            self.conn.setopt(pycurl.LOW_SPEED_LIMIT, 1)
            self.conn.setopt(pycurl.LOW_SPEED_TIME, self.timeout)
        self.conn.setopt(pycurl.URL, API_ENDPOINT_URL)
        self.conn.setopt(pycurl.USERAGENT, USER_AGENT)
        # Using gzip is optional but saves us bandwidth.
        self.conn.setopt(pycurl.ENCODING, 'deflate, gzip')
        self.conn.setopt(pycurl.POST, 1)
        self.conn.setopt(pycurl.POSTFIELDS, urllib.urlencode(POST_PARAMS))
        self.conn.setopt(pycurl.HTTPHEADER, ['Host: stream.twitter.com',
                                             'Authorization: %s' % self.get_oauth_header()])
        # self.handle_tweet is the method that are called when new tweets arrive
        self.conn.setopt(pycurl.WRITEFUNCTION, self.handle_tweet)

    def get_oauth_header(self):
        """ Create and return OAuth header.
        """
        params = {'oauth_version': '1.0',
                  'oauth_nonce': oauth.generate_nonce(),
                  'oauth_timestamp': int(time.time())}
        req = oauth.Request(method='POST', parameters=params, url='%s?%s' % (API_ENDPOINT_URL,
                                                                             urllib.urlencode(POST_PARAMS)))
        req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), self.oauth_consumer, self.oauth_token)
        return req.to_header()['Authorization'].encode('utf-8')

    def start(self):
        """ Start listening to Streaming endpoint.
        Handle exceptions according to Twitter's recommendations.
        """
        backoff_network_error = 0.25
        backoff_http_error = 5
        backoff_rate_limit = 60
        while True:
            self.setup_connection()
            try:
                self.conn.perform()
            except:
                # Network error, use linear back off up to 16 seconds
                print 'Network error: %s' % self.conn.errstr()
                print 'Waiting %s seconds before trying again' % backoff_network_error
                time.sleep(backoff_network_error)
                backoff_network_error = min(backoff_network_error + 1, 16)
                continue
            # HTTP Error
            sc = self.conn.getinfo(pycurl.HTTP_CODE)
            if sc == 420:
                # Rate limit, use exponential back off starting with 1 minute and double each attempt
                print 'Rate limit, waiting %s seconds' % backoff_rate_limit
                time.sleep(backoff_rate_limit)
                backoff_rate_limit *= 2
            else:
                # HTTP error, use exponential back off up to 320 seconds
                print 'HTTP error %s, %s' % (sc, self.conn.errstr())
                print 'Waiting %s seconds' % backoff_http_error
                time.sleep(backoff_http_error)
                backoff_http_error = min(backoff_http_error * 2, 320)

    def handle_tweet(self, data):
        """ This method is called when data is received through Streaming endpoint.
        """
        self.buffer += data
        if data.endswith('\r\n') and self.buffer.strip():
            # complete message received
            message = json.loads(self.buffer)
            self.buffer = ''
            msg = ''
            if message.get('limit'):
                print 'Rate limiting caused us to miss %s tweets' % (message['limit'].get('track'))
            elif message.get('disconnect'):
                raise Exception('Got disconnect: %s' % message['disconnect'].get('reason'))
            elif message.get('warning'):
                print 'Got warning: %s' % message['warning'].get('message')
            else:
                print 'Got tweet with text: %s' % message.get('text')


if __name__ == '__main__':
    ts = TwitterStream()
    ts.setup_connection()
    ts.start()