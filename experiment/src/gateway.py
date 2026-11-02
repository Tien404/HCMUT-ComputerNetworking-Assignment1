"""A minimal raw-HTTP server for the static UI shell."""

import argparse
import asyncio
import mimetypes
from pathlib import Path
from urllib.parse import urlsplit


UI_DIRECTORY = Path(__file__).resolve().parent.parent / "ui"
ALLOWED_FILES = {"index.html", "app.js", "style.css"}


async def handle_request(reader, writer):
    try:
        request_line = await asyncio.wait_for(reader.readline(), timeout=5)
        parts = request_line.decode("ascii", errors="replace").strip().split()
        if len(parts) != 3 or parts[0] != "GET":
            await respond(writer, 405, b"Only GET is supported")
            return

        path = urlsplit(parts[1]).path
        filename = "index.html" if path == "/" else path.lstrip("/")
        if filename not in ALLOWED_FILES:
            await respond(writer, 404, b"Not found")
            return

        while True:
            header = await asyncio.wait_for(reader.readline(), timeout=5)
            if header in (b"\r\n", b"\n", b""):
                break

        body = (UI_DIRECTORY / filename).read_bytes()
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        writer.write(
            f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}; charset=utf-8\r\n"
            f"Content-Length: {len(body)}\r\nConnection: close\r\n\r\n".encode("ascii")
            + body
        )
        await writer.drain()
    except (asyncio.TimeoutError, ConnectionError, OSError) as exc:
        print(f"HTTP request ended: {exc}")
    finally:
        writer.close()
        await writer.wait_closed()


async def respond(writer, status, body):
    reason = {404: "Not Found", 405: "Method Not Allowed"}[status]
    writer.write(
        f"HTTP/1.1 {status} {reason}\r\nContent-Type: text/plain; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\nConnection: close\r\n\r\n".encode("ascii") + body
    )
    await writer.drain()


async def run(host, port):
    server = await asyncio.start_server(handle_request, host, port)
    print(f"Static UI available at http://{host}:{port}")
    async with server:
        await server.serve_forever()


def main():
    parser = argparse.ArgumentParser(description="Serve the experiment's static UI")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    try:
        asyncio.run(run(args.host, args.port))
    except KeyboardInterrupt:
        print("\nGateway stopped.")


if __name__ == "__main__":
    main()
