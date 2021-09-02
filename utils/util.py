import json
import click
from uuid import UUID

def handleResponse(response, file_write):
    if file_write: 
        f = open("responses/last_response.json", "w")
        click.echo(prettyJson(response.text), file=f)
        click.echo(f"Response written to file: {f.name}")
        f.close()
    else: 
        click.echo(prettyJson(response.text))

def prettyJson(text):
    return json.dumps(json.loads(text), indent=4)


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)