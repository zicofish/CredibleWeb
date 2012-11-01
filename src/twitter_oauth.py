#!/usr/bin/env python
# coding: utf-8

import urllib
import random
import hmac
import binascii
import hashlib
import time
import conf

def create_twitter_signature(method, baseUrl, req_params, oauth_params, consumer_secret, token_secret = None):
    params = [(percent_code(k), percent_code(v)) for k,v in req_params.items()]
    params.extend([(percent_code(k), percent_code(v)) for k,v in oauth_params.items()])
    params.sort()
    param_string = '&'.join(['%s=%s' % (k, v) for k, v in params])
    sig = (method.upper(), percent_code(baseUrl), percent_code(param_string))
    signature_base_string = '&'.join(sig)
    signing_key = '%s&' % percent_code(consumer_secret)
    if token_secret:
        signing_key += percent_code(token_secret)
    hashed_value = hmac.new(signing_key, signature_base_string, hashlib.sha1).digest()
    return binascii.b2a_base64(hashed_value)[:-1]  

def percent_code(str):
    return urllib.quote(str, safe = '-._~')

def generate_nonce(length=8):
    """Generate pseudorandom number."""
    return ''.join([str(random.randint(0, 9)) for i in range(length)])

def generate_timestamp():
    """Get seconds since epoch (UTC)."""
    return str(int(time.time()))

def get_oauth_header(method, baseUrl, params, oauth_callback, 
                     consumer_key, consumer_secret, token=None, token_secret=None):
    if params == None:
        params = {}
    oauth_params = {}
    oauth_params['oauth_consumer_key'] = consumer_key
    oauth_params['oauth_nonce'] = generate_nonce()
    oauth_params['oauth_signature_method'] = 'HMAC-SHA1'
    oauth_params['oauth_timestamp'] = generate_timestamp()
    if token:
        oauth_params['oauth_token'] = token
    if oauth_callback:
        oauth_params['oauth_callback'] = oauth_callback
    oauth_params['oauth_version'] = '1.0'
    oauth_params['oauth_signature'] = create_twitter_signature(method, baseUrl,
                                                        params, oauth_params, 
                                                        consumer_secret, token_secret)
    header = 'OAuth '
    header += ', '.join(['%s="%s"' % (percent_code(k), percent_code(v))
                                      for k, v in oauth_params.items()])
    return header

if __name__ == '__main__':
    print get_oauth_header('POST', 'https://api.twitter.com/oauth/request_token', None, 
                           'http://localhost/sign-in-with-twitter/', 
                           'cChZNFj6T5R0TigYB9yd1w', 'L8qq9PZyRg6ieKGEKhZolGC0vJWLw8iEJ88DRdyOg')
    
    