import json
from json import JSONDecodeError
from typing import Generator

import pika


class Consumer:
    def __init__(self):
        credentials = pika.PlainCredentials("guest", "guest")
        self.conn_params = pika.ConnectionParameters(
            "localhost",
            credentials=credentials,
            client_properties={"connection_name": "SSE Test Consumer"},
        )
        self.channel = pika.BlockingConnection(self.conn_params).channel()
        self.channel.exchange_declare("sse", "fanout")
        self.callback = None

    def subscribe(self) -> Generator[str, str, None]:
        result = self.channel.queue_declare("", exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(queue_name, "sse")
        for method, props, body in self.channel.consume(queue_name):
            body = body.decode("utf-8")
            print(f"message received: {body}")
            self.channel.basic_ack(method.delivery_tag)
            try:
                data = json.loads(body)
                content = data["content"]
                event = data["event"]
                yield event, content
            except (KeyError, JSONDecodeError) as e:
                print(e)
                yield "unknown", body
