#!/usr/bin/env python
import firenado.conf
import pika
import logging
logger = logging.getLogger(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='ping_rpc_queue')


def on_request(ch, method, props, body):
    logger.info("Ping received from %s." % body)

    response = 'Pong'

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(
                         correlation_id=props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='ping_rpc_queue')

logger.info(" [x] Awaiting RPC Ping requests")
channel.start_consuming()