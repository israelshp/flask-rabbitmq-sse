# Server Sent Events with Flask + RabbitMQ Server
This is an example of using Flask and RabbitMQ in order to create server sent events.

For each new connection a new `Queue` is created. In another thread, messages from `sse` exchange are consumed and enqueued to each one of the connection queues. When a new message is enqueued, it is immediately sent to the client with `text/event-stream` content-type. 

## Usage
1. Run the server:
```shell
$ python app.py
```

2. Subscribe to events stream:
```shell
$ curl -s -N --http2 -H "Accept:text/event-stream" http://localhost:5000/events
```

3. Publish messages to an exchange named `sse` and they will be displayed in the client. The messages structure is:
```json
{
  "event": "information",
  "content": "foo"
}
```
Messages can be published via RabbitMQ management GUI or:
```shell
$ curl -X POST -d '{"event": "message", "content": "some content"}' -H "Content-Type:application/json"  http://localhost:5000/publish
```