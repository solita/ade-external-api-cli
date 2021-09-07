import click
from utils import util

@click.group()
@click.pass_context
def commits(ctx):
    ctx.obj['BASE_URL'] = f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/commits"


@commits.command()
@click.pass_context
@click.option('--id', required=True, type=int)
def get(ctx, id):
    s = ctx.obj['SESSION']
    response = s.get(f"{ctx.obj['BASE_URL']}/{id}")
    util.handleResponse(response.text, ctx.obj['FILE_WRITE'])
    return response


@commits.command()
@click.pass_context
@click.option('--id', required=True, type=int)
def content(ctx, id):
    s = ctx.obj['SESSION']
    response = s.get(f"{ctx.obj['BASE_URL']}/{id}/content")
    util.handleResponse(response.text, ctx.obj['FILE_WRITE'])
    return response