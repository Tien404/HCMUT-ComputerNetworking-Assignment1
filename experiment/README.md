# Client-Server Collaboration Prototype

This folder is an independent starting point for the client/server experiment.
It uses Python's standard library and raw TCP/UDP sockets through `asyncio`.

## Run

Start the server:

```bash
python3 -m src.server
```

In another terminal, start a client with a unique username:

```bash
python3 -m src.client
```

The server listens on TCP and UDP port `9000` by default. To change it, pass
`--host` and `--port` to the server and `--server` and `--port` to the client.
The first version supports a TCP handshake, username-only UDP login, online
user lists, heartbeat messages, and server-relayed chat. Username-only login
is for local experimentation, not real authentication.

The static UI shell can be served separately:

```bash
python3 -m src.gateway
```

It listens on `127.0.0.1:8080`. It is only a static page at this stage; it is
not connected to the client yet.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Current layout

```text
src/
  server.py          TCP handshake, UDP login, presence, and chat relay
  client.py          CLI client
  protocol.py        Small versioned JSON packet format
  file_transfer.py   File chunking and SHA-256 helpers
  gateway.py         Minimal raw-HTTP static file server for the UI
ui/
  index.html
  app.js
  style.css
tests/
```

File transfer and the UI-to-client connection are the next implementation
steps. The current UDP chat is a learning prototype and does not yet provide
retransmission, encryption, or durable delivery guarantees.
