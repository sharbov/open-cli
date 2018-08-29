import json
import tabulate

JSON = "json"
TABLE = "table"


def to_table(response):
    """Convert raw response into table output."""
    if response is None:
        return response

    # Tabulate dictionary responses
    if isinstance(response, dict):
        return tabulate.tabulate(
            [(key, value) for key, value in response.items()],
            headers={"Field": "Field", "Value": "Value"},
            tablefmt='grid'
        )

    # Tabulate list responses
    if isinstance(response, list):
        return tabulate.tabulate(
            response,
            headers={key: key.capitalize() for key in response[0].keys()},
            tablefmt='grid'
        )


def to_json(response):
    """Convert raw response into json output."""
    return json.dumps(response, indent=2)


FORMATTERS = {
    JSON: to_json,
    TABLE: to_table,
}


def format_response(response, output_format):
    return u"\n{}\n".format(FORMATTERS[output_format](response))
