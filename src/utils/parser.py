from urllib.parse import parse_qs


class Parser:
    @staticmethod
    def parse_form_data(environ: dict) -> dict:
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(content_length).decode('utf-8')

        form_data = parse_qs(body)
        parsed_data = {key: value[0] for key, value in form_data.items()}

        return parsed_data

    @staticmethod
    def parse_query_data(environ: dict) -> dict:
        query_string = environ.get('QUERY_STRING', '')
        query_params = parse_qs(query_string)
        parsed_params = {key: value[0] if len(value) == 1 else value for key, value in query_params.items()}
        return parsed_params
