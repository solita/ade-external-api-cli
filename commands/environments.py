import click
import json
import time

from click.utils import echo
from commands import deployments
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
    response = get_instance(ctx, environment_name, instance_id)
    if response.status_code == 200:
        util.handleResponse(response.text, ctx.obj['FILE_WRITE'])
        exit(0)
    elif response.text != None:
        click.echo(f"{util.prettyJson(response.text)}", err=True)
    exit(1)


@environments.command()
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--instance-id', required=True, type=click.UUID)
def deploy(ctx, environment_name, instance_id):
    s = ctx.obj['SESSION']
    request_url = f"{ctx.obj['BASE_URL']}/{environment_name}/instances/{instance_id}/deployments"
    response = s.post(request_url)

    deployment = json.loads(response.text)
    phases = json.loads(deployments.get_phases(ctx, deployment["id"]).text)

    progress = 0
    with click.progressbar(length=len(phases), label='Deployment progress') as bar:
        while deployment["state"] in ["WAITING", "RUNNING"]:
            time.sleep(2)
            deployment = json.loads(deployments.get_deployment(ctx, deployment["id"]).text)
            phases = json.loads(deployments.get_phases(ctx, deployment["id"]).text)
            successes = 0
            for phase in phases:
                if phase["state"] not in ["WAITING", "RUNNING"]:
                    successes += 1
            bar.update(successes - progress)
            progress = successes

    deployments.log_phases(phases)
    util.handleResponse(deployment, ctx.obj['FILE_WRITE'])
    return response


def get_instance(ctx, environment_name, instance_id):
    s = ctx.obj['SESSION']
    request_url =  f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/environments/{environment_name}/instances/{instance_id}"
    return s.get(request_url)