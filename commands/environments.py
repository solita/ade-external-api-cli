import click
from utils import util

@click.group()
@click.pass_context
def environments(ctx):
    ctx.obj['BASE_URL'] = f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/environments"


@environments.command()
@click.pass_context
@click.option('--environment-name', required=True)
def get(ctx, environment_name):
    s = ctx.obj['SESSION']
    request_url = f"{ctx.obj['BASE_URL']}/{environment_name}"
    response = s.get(request_url)
    util.handleResponse(response.text, ctx.obj['FILE_WRITE'])
    return response


@environments.command()
@click.pass_context
@click.option('--environment-name', required=True)
def instances(ctx, environment_name):
    s = ctx.obj['SESSION']
    request_url = f"{ctx.obj['BASE_URL']}/{environment_name}/instances"
    response = s.get(request_url)
    util.handleResponse(response.text, ctx.obj['FILE_WRITE'])
    return response


@environments.command()
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--instance-id', required=True, type=click.UUID)
def instance(ctx, environment_name, instance_id):
    s = ctx.obj['SESSION']
    request_url = f"{ctx.obj['BASE_URL']}/{environment_name}/instances/{instance_id}"
    response = s.get(request_url)
    util.handleResponse(response.text, ctx.obj['FILE_WRITE'])
    return response

@environments.command()
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--instance-id', required=True, type=click.UUID)
def deploy(ctx, environment_name, instance_id):
    s = ctx.obj['SESSION']
    request_url = f"{ctx.obj['BASE_URL']}/{environment_name}/instances/{instance_id}/deployments"
    response = s.post(request_url)
    util.handleResponse(response.text, ctx.obj['FILE_WRITE'])
    return response