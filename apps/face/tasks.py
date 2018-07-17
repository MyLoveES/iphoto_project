# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from kombu import Queue
from pykafka import KafkaClient
import json


# @shared_task
# def kafka_produce(message):
#     client = KafkaClient(hosts="106.15.191.61:9092")
#     topic = client.topics["iphoto_entity"]
#     with topic.get_producer(delivery_reports=True) as producer:
#         producer.produce(message)
#         msg, exc = producer.get_delivery_report(block=False)
#         try:
#             msg, exc = producer.get_delivery_report(block=False)
#             if exc is not None:
#                 print('Failed to deliver msg {}: {}'.format(msg.partition_key, repr(exc)))
#                 return False
#             else:
#                 print('Successfully delivered msg {}'.format(msg.partition_key))
#                 return True
#         except Queue.Empty:
#             print('Queue Empty ERROR')
#     return Fa



@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)