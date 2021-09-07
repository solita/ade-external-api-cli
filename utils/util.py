import json
import click
from uuid import UUID

def handleResponse(content, file_write):
    if file_write: 
        f = open(f"responses/{file_write}", "w")
        click.echo(prettyJson(content), file=f)
        click.echo(f"Response written to file: {f.name}")
        f.close()
    else: 
        click.echo(prettyJson(content))

def prettyJson(text):
    return json.dumps(json.loads(text), indent=4)


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)