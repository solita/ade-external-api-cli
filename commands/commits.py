import click
import json
from utils import util


@click.group()
def commits():
    pass


@commits.command()
@click.pass_context
@click.option('--id', required=True, type=int)
def get(ctx, id):
    response = get_commit(ctx, id)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


@commits.command()
@click.pass_context
@click.option('--id', required=True, type=int)
def content(ctx, id):
    response = get_content(ctx, id)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


def get_commit(ctx, id):
    s = ctx.obj['SESSION']
    response = s.get(
        f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/commits/{id}")
    content = json.loads(response.text) if response.text else ""

    if response.status_code != 200:
        click.echo(
            f"Unable to fetch commit with id {id}. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    elif response.status_code != 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    return content


def get_content(ctx, id):
    s = ctx.obj['SESSION']
    response = s.get(
        f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/commits/{id}/content")
    content = json.loads(response.text) if response.text else ""

    if response.status_code != 200:
        click.echo(
            f"Unable to fetch commit content with id {id}. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    elif response.status_code != 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    return content
