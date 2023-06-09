import json
from json import JSONDecodeError
from typing import Generator, Tuple

import pika

from logger import logger


class MessageBroker:
    EXCHANGE_NAME = "sse"

    def __init__(self):
        credentials = pika.PlainCredentials("guest", "guest")
        self.conn_params = pika.ConnectionParameters(
            "localhost",
            credentials=credentials,
            client_properties={"connection_name": "SSE Test"},
        )
        self.channel = pika.BlockingConnection(self.conn_params).channel()
        self.channel.exchange_declare(self.EXCHANGE_NAME, "fanout")
        self.callback = None

    def subscribe(self) -> Generator[Tuple[int, str, str], None, None]:
        result = self.channel.queue_declare("", exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(queue_name, self.EXCHANGE_NAME)
        for method, props, body in self.channel.consume(queue_name):
            body = body.decode("utf-8")
            logger.info(f"<<< message received: {body}")
            self.channel.basic_ack(method.delivery_tag)
            id = method.delivery_tag
            try:
                data = json.loads(body)
                content = data["content"]
                event = data["event"]
                yield id, event, content
            except (KeyError, JSONDecodeError) as e:
                yield id, "message", body

    def publish(self, content: str, event: str):
        data = {"event": event, "content": content}
        data_bytes = str.encode(json.dumps(data))
        self.channel.basic_publish(self.EXCHANGE_NAME, "", data_bytes)
