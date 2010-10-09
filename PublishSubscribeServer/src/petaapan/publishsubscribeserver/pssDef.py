# -*- coding: utf-8 -*-
'''
Common definitions used in the PublishSubscribeServer GAC application
Created on 2010-08-29

@author: jonathan
'''

REQ_SUBSCRIPTION = 'subscription' # Identifies the subscription data in
                                  # the JSON subscription message
REQ_PORT = 'port' # Port used to communicate to Google Apps
REQ_PUBLISHER = 'publisher' # Google App path that accesses publisher module
SUBACTION = 'subscribe' # Relative URL to Google Apps handler for subscription
SUBSCRIBER = 'subscriber' # URL where subscriber wishes to receive notifications
                          # Used in notification message
USER_ID = 'userid' # Google Id
FIRST_NAME = 'firstName' # Subscriber's first name
MIDDLE_NAME = 'middleName' # Subscriber's middle name
LAST_NAME = 'lastName' # Subscriber's last name
SUBSCRIBER_DNS = 'subscriberDns' # DNS address where subscriber wants to 
                                 # receive notifications
SUBSCRIBER_PORT = 'subscriberPort' # Port where subscriber wishes to
                                   # receive notifications
SUBSCRIBE = 1 # User is subscribing to a specified publisher
UNSUBSCRIBE = 0 # User is un-subscribing from a specified publisher
TESTING = 'Testing' # Tell server this is a test subscription
TEST_SUBSCRIBED = 'subscribed'
TEST_UNSUBSCRIBED = 'unsubscribed'
GITHUB_NOTIFICATION = 'Github Notification'
