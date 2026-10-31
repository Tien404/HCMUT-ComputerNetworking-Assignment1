from src.common.constants import HTTP_PORT


def handle_request(request, client_state):
    # TODO: Serve UI/state/events via GET; enqueue login/chat/file commands via POST.
    # Validate Content-Length and paths; enforce size limits, partial I/O and timeouts.
    pass


async def serve(client_state, host="127.0.0.1", port=HTTP_PORT):
    # TODO: Use asyncio.start_server with raw HTTP parsing.
    # Read snapshots and enqueue commands; handlers must not mutate session state.
    pass
