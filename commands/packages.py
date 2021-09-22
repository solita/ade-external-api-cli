import click
import json
from utils import util

@click.group()
def packages():
    """
    Functionality related to packages.
    """
    pass

@packages.command()
@click.pass_context
def list(ctx):
    """
    Lists all packages
    """
    response = list_packages(ctx)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))

def list_packages(ctx):
    s = ctx.obj['SESSION']
    response = s.get(
        f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/packages")
    content = json.loads(response.text) if response.text else ""
    if response.status_code == 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    elif response.status_code != 200:
        click.echo(
            f"Unable to fetch packages. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    return content