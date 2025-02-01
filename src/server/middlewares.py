import logging

logger = logging.getLogger("middleware")


def CORSMiddleware(
    app, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
):
    def middleware(environ, start_response):
        headers = [
            ("Access-Control-Allow-Origin", ",".join(allow_origins)),
            ("Access-Control-Allow-Credentials", "true" if allow_credentials else "false"),
            ("Access-Control-Allow-Methods", ",".join(allow_methods)),
            ("Access-Control-Allow-Headers", ",".join(allow_headers)),
        ]

        if environ["REQUEST_METHOD"] == "OPTIONS":
            start_response("200 OK", headers)
            return [b""]

        return app(environ, start_response)

    return middleware


def log_request_middleware(app):
    def middleware(environ, start_response):
        logger.info(f"{environ['REQUEST_METHOD']} {environ['PATH_INFO']}")
        return app(environ, start_response)

    return middleware
