from flask import Flask, Response

from consumer import Consumer

app = Flask(__name__)


def event_stream():
    consumer = Consumer()
    for event, content in consumer.subscribe():
        yield f"event:{event}\ndata: {content}\n\n"


@app.route("/")
def index():
    return "ok"


@app.route("/events")
def events():
    print("new subscription")
    return Response(event_stream(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True)
