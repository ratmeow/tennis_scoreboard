import os


class WSGIApp:
    def __init__(self, router, static_dir="static"):
        self.router = router
        self.static_dir = static_dir
        self.middlewares = []

    def add_middleware(self, middleware):
        self.middlewares.append(middleware)

    def serve_static(self, environ, start_response):
        file_path = environ["PATH_INFO"].lstrip("/")  # Убираем '/'
        full_path = os.path.join(self.static_dir, file_path)

        if os.path.exists(full_path) and os.path.isfile(full_path):
            content_type = "text/plain"
            if full_path.endswith(".css"):
                content_type = "text/css"
            elif full_path.endswith(".js"):
                content_type = "application/javascript"

            start_response("200 OK", [("Content-Type", content_type)])
            with open(full_path, "rb") as f:
                return [f.read()]

        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return [b"File not found"]

    def __call__(self, environ, start_response):
        handler = self.router
        for middleware in reversed(self.middlewares):
            handler = middleware(handler)

        if environ["PATH_INFO"].startswith("/static/"):
            return self.serve_static(environ, start_response)

        return handler(environ, start_response)
