import time
import uuid
from queue import Queue
from threading import Thread
from typing import Generator

from flask import Flask, Response, request, render_template

from messagebroker import MessageBroker
from logger import logger

app = Flask(__name__)
broker = MessageBroker()
connections: dict[uuid.UUID, Queue] = {}


def stats() -> None:
    while True:
        count = len(connections)
        be_verb = "are" if count != 1 else "is"
        suffix = "s" if count != 1 else ""
        logger.info(f"{count} client{suffix} {be_verb} connected to events stream")
        time.sleep(30)


def consume() -> None:
    for eid, event, content in broker.subscribe():
        for q in connections.values():
            q.put((eid, event, content))


def event_stream(user_id: uuid.UUID) -> Generator[str, None, None]:
    q = Queue()
    connections[user_id] = q
    try:
        while True:
            eid, event, content = q.get()
            logger.info(f">>> notifying {user_id}")
            yield f"id:{eid}\nevent:{event}\ndata: {content}\n\n"
    finally:
        logger.info(f"{user_id} has disconnected")
        connections.pop(user_id)


@app.route("/events")
def events() -> Response:
    user_id = uuid.uuid4()
    logger.info(
        f"new subscription: {user_id} ({request.remote_addr}, {request.user_agent})"
    )
    return Response(event_stream(user_id), mimetype="text/event-stream")


@app.route("/")
def viewer() -> str:
    return render_template("viewer.html")


@app.route("/publish", methods=["POST"])
def publish() -> Response:
    data = request.json
    event = data.get("event", "message")
    content = data.get("content")
    broker.publish(content, event)
    return Response("ok", 200)


if __name__ == "__main__":
    logger.info("Starting consumer...")
    consumer_thread = Thread(target=consume, name="RabbitMQ Consumer")
    consumer_thread.start()

    logger.info("Starting stats...")
    stats_thread = Thread(target=stats, name="Stats")
    stats_thread.start()

    logger.info("Starting server...")
    app.run(use_reloader=False)
