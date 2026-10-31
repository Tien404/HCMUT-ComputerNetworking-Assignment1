# Client-Server Collaboration Application

Network Application Development assignment for messaging and file sharing using
a custom application-layer protocol over UDP.

## Requirements

- Python 3
- Dependencies listed in `requirements.txt`

## Setup

Run these commands from the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

On Windows, use `.venv\Scripts\activate` to activate the environment.

## Configuration checks

```bash
# Server
python3 -B -m src.server --check

# Client A
python3 -B -m src.client.main --udp-port 9100 --http-port 8080 --check

# Client B
python3 -B -m src.client.main --udp-port 9101 --http-port 8081 --check
```

The default server address is `127.0.0.1:9000`. These commands only check
configuration; they do not open sockets or start the application yet.

## Tests

```bash
python3 -B -m unittest discover -s tests -v
```

## Project structure

```text
src/
  server.py    Server, login, online users, and message forwarding
  client/      Client, file transfer, and local HTTP interface
  common/      Constants, enums, shared errors, and security
  protocol/    Packets, reliability, flow control, and congestion control
ui/            HTML, CSS, and JavaScript
tests/        Basic tests and test placeholders
docs/         Assignment, diagrams, and report
```
