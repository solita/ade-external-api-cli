import click
import json
from utils import util


@click.group()
def deployments():
    pass


@deployments.command()
@click.pass_context
@click.option('--id', required=True, type=click.UUID)
def get(ctx, id):
    response = get_deployment(ctx, id)
    if response.status_code == 200:
        util.handleResponse(response.text, ctx.obj['FILE_WRITE'])
        return response
    elif response.text != None:
        click.echo(f"{util.prettyJson(response.text)}", err=True)
    exit(1)


@deployments.command()
@click.pass_context
@click.option('--id', required=True, type=click.UUID)
def phases(ctx, id):
    response = get_phases(ctx, id)
    if response.status_code == 200:
        if (ctx.obj['FILE_WRITE'] != None):
            util.handleResponse(response.text, ctx.obj['FILE_WRITE'])
        else:
            log_phases(json.loads(response.text))
        return response
    elif response.text != None:
        click.echo(f"{util.prettyJson(response.text)}", err=True)
    exit(1)


def get_deployment(ctx, id):
    s = ctx.obj['SESSION']
    return s.get(f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/deployments/{id}")


def get_phases(ctx, id):
    s = ctx.obj['SESSION']
    return s.get(f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/deployments/{id}/phases")


def log_phases(phases):
    for phase in phases:
        if phase["state"] == "SUCCESS":
            click.echo(f"{click.style(phase['packageName'], bold=True)} > {click.style(phase['state'], fg='green')}", err=True)
        elif phase["state"] == "FAILED":
            click.echo(f"{click.style(phase['packageName'], bold=True)} > {click.style(phase['state'], fg='red')}", err=True)
        else:
            click.echo(f"{click.style(phase['packageName'], bold=True)} > {phase['state']}", err=True)
