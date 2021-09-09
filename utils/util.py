import json
import click
import os
from uuid import UUID

def write_to_file(dir, file_name, content):
    if dir: path =f"responses/{dir}"
    else: path = "responses"

    if not os.path.exists(path):
        os.makedirs(path)

    with open(f"{path}/{file_name}", "w") as file:
        click.echo(pretty_json(content), file=file)


def pretty_json(content):
    return json.dumps(content, indent=4)


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)