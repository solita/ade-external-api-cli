import click
import json
import time

from commands import deployments
from utils import util


@click.group()
def environments():
    """
    Functionality related to environments.
    """
    pass


@environments.command()
@click.pass_context
@click.option('--environment-name', required=True)
def get(ctx, environment_name):
    """
    Gets information about an environment
    """
    response = get_environment(ctx, environment_name)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


@environments.command()
@click.pass_context
@click.option('--environment-name', required=True)
def instances(ctx, environment_name):
    """
    Gets all target instances of an environment
    """
    response = list_instances(ctx, environment_name)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


@environments.command()
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--instance-id', required=True, type=click.UUID)
def instance(ctx, environment_name, instance_id):
    """
    Gets information about a target instance
    """
    response = get_instance(ctx, environment_name, instance_id)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


@environments.command()
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--instance-id', required=True, type=click.UUID)
def deploy(ctx, environment_name, instance_id):
    """
    Deploys all promoted packages in a target instance
    """
    deployment = deploy_promotions(ctx, environment_name, instance_id)
    phases = deployments.get_phases(ctx, deployment["id"])

    progress = 0
    with click.progressbar(length=len(phases), label='Deployment progress') as bar:
        while deployment["state"] in ["WAITING", "RUNNING"]:
            time.sleep(2)
            deployment = deployments.get_deployment(ctx, deployment["id"])
            phases = deployments.get_phases(ctx, deployment["id"])
            successes = 0
            for phase in phases:
                if phase["state"] not in ["WAITING", "RUNNING"]:
                    successes += 1
            bar.update(successes - progress)
            progress = successes

    deployments.log_phases(phases)

    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", deployment)
    else:
        click.echo(util.pretty_json(deployment))


def get_environment(ctx, environment_name):
    s = ctx.obj['SESSION']
    response = s.get(
        f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/environments/{environment_name}")
    content = json.loads(response.text) if response.text else ""
    if response.status_code == 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    elif response.status_code != 200:
        click.echo(
            f"Unable to fetch environment with name {environment_name}. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    return content


def list_instances(ctx, environment_name):
    s = ctx.obj['SESSION']
    response = s.get(
        f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/environments/{environment_name}/instances")
    content = json.loads(response.text) if response.text else ""
    if response.status_code == 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    elif response.status_code != 200:
        click.echo(
            f"Unable to fetch instances with environment name {environment_name}. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    return content


def get_instance(ctx, environment_name, instance_id):
    s = ctx.obj['SESSION']
    response = s.get(
        f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/environments/{environment_name}/instances/{instance_id}")
    content = json.loads(response.text) if response.text else ""
    if response.status_code == 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    elif response.status_code != 200:
        click.echo(
            f"Unable to fetch instance with environment name {environment_name} and instance id {instance_id}. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    return content


def deploy_promotions(ctx, environment_name, instance_id):
    s = ctx.obj['SESSION']
    response = s.post(
        f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/environments/{environment_name}/instances/{instance_id}/deployments")
    content = json.loads(response.text) if response.text else ""
    if response.status_code == 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    elif response.status_code != 200:
        click.echo(
            f"Unable to initialize deployment with environment name {environment_name} and instance id {instance_id}. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    return content
