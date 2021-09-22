import click
import json
from utils import util


@click.group()
def commits():
    """
    Functionality related to commits.
    """
    pass


@commits.command()
@click.pass_context
@click.option('--package-id', type=click.UUID)
@click.option('--package-name')
@click.option('--message')
@click.option('--author')
@click.option('--deleted', type=click.BOOL)
@click.option('--committed-from')
@click.option('--committed-to')
@click.option('--size', type=int)
@click.option('--page', type=int)
def list(ctx, package_id, package_name, message, author, deleted, committed_from, committed_to, size, page):
    """
    Gets all promotions with given filters
    """
    response = list_commits(ctx, package_id, package_name, message, author, deleted, committed_from, committed_to, size, page)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


@commits.command()
@click.pass_context
@click.option('--id', required=True, type=int)
def get(ctx, id):
    """
    Gets information about a commit
    """
    response = get_commit(ctx, id)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


@commits.command()
@click.pass_context
@click.option('--id', required=True, type=int)
def content(ctx, id):
    """
    Gets full content of a commit
    """
    response = get_content(ctx, id)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))

def list_commits(ctx, package_id, package_name, message, author, deleted, committed_from, committed_to, size, page):
    s = ctx.obj['SESSION']

    params = []
    if package_id:
        params.append(f"packageId={package_id}")
    if package_name:
        params.append(f"packageName={package_name}")
    if message:
        params.append(f"message={message}")
    if author:
        params.append(f"author={author}")
    if deleted:
        params.append(f"deleted={deleted}")
    if committed_from:
        params.append(f"committedFrom={committed_from}")
    if committed_to:
        params.append(f"committedTo={committed_to}")
    if size:
        params.append(f"size={size}")
    if page:
        params.append(f"page={page}")

    request_url = f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/commits"
    if len(params) != 0:
        request_url = f"{request_url}?" + "&".join(params)

    response = s.get(request_url)
    content = json.loads(response.text) if response.text else ""

    if response.status_code == 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    elif response.status_code != 200:
        click.echo(
            f"Unable to list promotions with given parameters. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    return content


def get_commit(ctx, id):
    s = ctx.obj['SESSION']
    response = s.get(
        f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/commits/{id}")
    content = json.loads(response.text) if response.text else ""

    if response.status_code == 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    elif response.status_code != 200:
        click.echo(
            f"Unable to fetch commit with id {id}. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    return content


def get_content(ctx, id):
    s = ctx.obj['SESSION']
    response = s.get(
        f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/commits/{id}/content")
    content = json.loads(response.text) if response.text else ""

    if response.status_code == 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    elif response.status_code != 200:
        click.echo(
            f"Unable to fetch commit content with id {id}. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    return content
