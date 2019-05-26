# fetch-metadata-asgi

Proof-of-concept [ASGI](https://asgi.readthedocs.io/en/latest/) middleware implementation of the **Fetch Metadata** specification for Python 3.6+.

The Fetch Metadata spec allows a server to reject a cross-origin request to protect clients from CSRF, XSSI and other bugs.

> **Important**: this repo was created following a talk by Lukas Weichselbaum at PyConWeb 2019. **It is _NOT_ an official nor audited implementation of the Fetch-Metadata specification in any way.** Feel free to fork it, copy-paste the code, or hack it away!

For more information:

- [Fetch Metadata | Chrome Platform Status](https://www.chromestatus.com/feature/5155867204780032)
- [WSGI implementation](https://github.com/empijei/sec-fetch-resource-isolation/blob/master/python/resource_isolation_middleware.py#L35)
- [Initiating discussion on Twitter](https://twitter.com/FlorimondManca/status/1132565224450592768)

## Installation

HTTP header parsing is provided by [Starlette](https://www.starlette.io):

```bash
pip install starlette
```

## Usage

This middleware should be usable with any ASGI3-compliant application.

An example "Hello, World!" ASGI app wrapped by the `FetchMetadataMiddleware` is provided in `example.py`:

```python
from fetch_metadata import FetchMetadataMiddleware
from starlette.responses import PlainTextResponse

async def app(scope, receive, send):
    assert scope["type"] == "http"
    response = PlainTextResponse("Hello, world!")
    await response(scope, receive, send)

app = FetchMetadataMiddleware(app)
```

Serve it using [uvicorn](https://www.uvicorn.org) or any other ASGI web server:

```bash
uvicorn example:app
```

Example allowed requests:

```bash
curl http://localhost:8000
curl http://localhost:8000 -H "Sec-Fetch-Site: cross-origin" -H "Sec-Fetch-Mode: navigate"
curl http://localhost:8000 -H "Sec-Fetch-Site: same-site"
```

Example disallowed requests:

```bash
curl http://localhost:8000 -H "Sec-Fetch-Site: cross-origin" -H "Sec-Fetch-Mode: cors"
```
