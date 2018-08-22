# -*- coding: utf-8 -*-

import boto3


class SnsClient(object):
    instance = None

    @classmethod
    def get(cls):
        if not cls.instance:
            cls.instance = SnsClient()
        return cls.instance

    def __init__(self):
        self.sns = boto3.resource('sns')

    def publish_event(self, topic_arn, subject, message, attributes={}):
        topic = self.sns.Topic(topic_arn)
        return topic.publish(Message=message,
                             MessageAttributes=attributes,
                             Subject=subject)
