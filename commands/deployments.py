import click
from utils import util

@click.group()
@click.pass_context
def deployments(ctx):
    ctx.obj['BASE_URL'] = f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/deployments"


@deployments.command()
@click.pass_context
@click.option('--id', required=True, type=click.UUID)
def get(ctx, id):
    s = ctx.obj['SESSION']
    response = s.get(f"{ctx.obj['BASE_URL']}/{id}")
    util.handleResponse(response.text, ctx.obj['FILE_WRITE'])
    return response


@deployments.command()
@click.pass_context
@click.option('--id', required=True, type=click.UUID)
def phases(ctx, id):
    s = ctx.obj['SESSION']
    response = s.get(f"{ctx.obj['EXTERNAL_API_URL']}/{id}/phases")
    util.handleResponse(response.text, ctx.obj['FILE_WRITE'])
    return response