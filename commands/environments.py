import json
import click
from utils import util

@click.group()
def environments():
    pass


@environments.command()
@click.pass_context
@click.option('--environment-name', required=True)
def get(ctx, environment_name):
    s = ctx.obj['SESSION']
    request_url = ctx.obj['EXTERNAL_API_URL'] + "/deployment/v1/environments/" + environment_name
    response = s.get(request_url)
    util.handleResponse(response, ctx.obj['FILE_WRITE'])
    return response


@environments.command()
@click.pass_context
@click.option('--environment-name', required=True)
def instances(ctx, environment_name):
    s = ctx.obj['SESSION']
    request_url = ctx.obj['EXTERNAL_API_URL'] + "/deployment/v1/environments/" + environment_name + "/instances"
    response = s.get(request_url)
    util.handleResponse(response, ctx.obj['FILE_WRITE'])
    return response


@environments.command()
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--instance-id', required=True, type=click.UUID)
def instance(ctx, environment_name, instance_id):
    s = ctx.obj['SESSION']
    request_url = ctx.obj['EXTERNAL_API_URL'] + "/deployment/v1/environments/" + environment_name + "/instances/" + str(instance_id)
    response = s.get(request_url)
    util.handleResponse(response, ctx.obj['FILE_WRITE'])
    return response

@environments.command()
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--instance-id', required=True, type=click.UUID)
def deploy(ctx, environment_name, instance_id):
    s = ctx.obj['SESSION']
    request_url = ctx.obj['EXTERNAL_API_URL'] + "/deployment/v1/environments/" + environment_name + "/instances/" + str(instance_id) + "/deployments"
    response = s.post(request_url)
    util.handleResponse(response, ctx.obj['FILE_WRITE'])
    return response