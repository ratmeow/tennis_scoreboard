class Router:
    def __init__(self):
        self.routes = {}

    def get(self, path):
        def decorator(func):
            normalized_path = path.rstrip('/')
            self.routes[("GET", normalized_path)] = func
            return func

        return decorator

    def post(self, path):
        def decorator(func):
            normalized_path = path.rstrip('/')
            self.routes[("POST", normalized_path)] = func
            return func

        return decorator

    def __call__(self, environ, start_response):
        method: str = environ["REQUEST_METHOD"]
        path: str = environ["PATH_INFO"]

        normalized_path = path.rstrip('/')

        route = self.routes.get((method, normalized_path))
        if route:
            return route(environ, start_response)

        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return [b"Page not found"]