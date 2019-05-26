from fetch_metadata import FetchMetadataMiddleware
from starlette.responses import PlainTextResponse


async def app(scope, receive, send):
    assert scope["type"] == "http"
    response = PlainTextResponse("Hello, world!")
    await response(scope, receive, send)


app = FetchMetadataMiddleware(app)
