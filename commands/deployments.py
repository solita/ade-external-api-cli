import json
import click
from utils import util

@click.group()
def deployments():
    pass


@deployments.command()
@click.pass_context
@click.option('--id', required=True, type=click.UUID)
def get(ctx, id):
    s = ctx.obj['SESSION']
    request_url = ctx.obj['EXTERNAL_API_URL'] + "/deployment/v1/deployments/" + str(id)
    response = s.get(request_url)
    util.handleResponse(response, ctx.obj['FILE_WRITE'])
    return response


@deployments.command()
@click.pass_context
@click.option('--id', required=True, type=click.UUID)
def phases(ctx, id):
    s = ctx.obj['SESSION']
    request_url = ctx.obj['EXTERNAL_API_URL'] + "/deployment/v1/deployments/" + str(id) + "/phases"
    response = s.get(request_url)
    util.handleResponse(response, ctx.obj['FILE_WRITE'])
    return response