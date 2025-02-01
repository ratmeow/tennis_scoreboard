from jinja2 import Environment, FileSystemLoader


class Renderer:
    def __init__(self, templates_dir: str = "src/frontend"):
        self.env = Environment(loader=FileSystemLoader(templates_dir))

    def render_template(
        self,
        template_name="index.html",
        context=None,
        status="200",
        content_type="text/html",
        start_response=None,
    ):
        if context is None:
            context = {}
        template = self.env.get_template(template_name)
        response_body = template.render(context)
        start_response(status, [("Content-Type", content_type)])
        return [response_body.encode("utf-8")]
