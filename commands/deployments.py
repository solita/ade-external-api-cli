import click
import json
from utils import util


@click.group()
def deployments():
    """
    Functionality related to deployments.
    """
    pass


@deployments.command()
@click.pass_context
@click.option('--id', required=True, type=click.UUID)
def get(ctx, id):
    """
    Gets information about a deployment
    """
    response = get_deployment(ctx, id)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


@deployments.command()
@click.pass_context
@click.option('--id', required=True, type=click.UUID)
def phases(ctx, id):
    """
    Gets information about phases of a deployment
    """
    response = get_phases(ctx, id)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        log_phases(response)


def get_deployment(ctx, id):
    s = ctx.obj['SESSION']
    response = s.get(
        f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/deployments/{id}")
    content = json.loads(response.text) if response.text else ""
    if response.status_code != 200:
        click.echo(
            f"Unable to fetch deployment with id {id}. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    elif response.status_code != 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    return content


def get_phases(ctx, id):
    s = ctx.obj['SESSION']
    response = s.get(
        f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/deployments/{id}/phases")
    content = json.loads(response.text) if response.text else ""
    if response.status_code != 200:
        click.echo(
            f"Unable to fetch deployment phases with id {id}. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    elif response.status_code != 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    return content


def log_phases(phases):
    for phase in phases:
        if phase["state"] == "SUCCESS":
            click.echo(
                f"{click.style(phase['packageName'], bold=True)} > {click.style(phase['state'], fg='green')}", err=True)
        elif phase["state"] == "FAILED":
            click.echo(
                f"{click.style(phase['packageName'], bold=True)} > {click.style(phase['state'], fg='red')}", err=True)
        else:
            click.echo(
                f"{click.style(phase['packageName'], bold=True)} > {phase['state']}", err=True)
