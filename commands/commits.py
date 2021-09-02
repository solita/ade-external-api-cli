import click
from utils import util

@click.group()
def commits():
    pass


@commits.command()
@click.pass_context
@click.option('--id', required=True, type=int)
def get(ctx, id):
    s = ctx.obj['SESSION']
    request_url = ctx.obj['EXTERNAL_API_URL'] + "/deployment/v1/commits/" + str(id)
    response = s.get(request_url)
    util.handleResponse(response, ctx.obj['FILE_WRITE'])
    return response


@commits.command()
@click.pass_context
@click.option('--id', required=True, type=int)
def content(ctx, id):
    s = ctx.obj['SESSION']
    request_url = ctx.obj['EXTERNAL_API_URL'] + "/deployment/v1/commits/" + str(id) + "/content"
    response = s.get(request_url)
    util.handleResponse(response, ctx.obj['FILE_WRITE'])
    return response