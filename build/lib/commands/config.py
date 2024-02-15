import click
import os
import json
from utils import util


@click.group()
def config():
    """
    Used to configure credentials for the tool usage.
    """
    pass


@config.command()
@click.pass_context
@click.option('--tenant', required=True)
@click.option('--installation', required=True)
@click.option('--environment', required=True)
@click.option('--apikey-id', required=True)
@click.option('--apikey-secret', required=True)
def add(ctx, tenant, installation, environment, apikey_id, apikey_secret):
    """
    Used to add new or modify old credentials in the configuration
    """

    config = {}
    if os.path.exists(ctx.obj['CONFIG_PATH']):
        with open(ctx.obj['CONFIG_PATH'], 'r') as file:
            config = json.loads(file.read())

    new_config = {
        "tenants": {
            tenant: {
                "installations": {
                    installation: {
                        "environments": {
                            environment: {
                                "type": "design" if environment == "design" else "runtime",
                                "apikey_id": apikey_id,
                                "apikey_secret": apikey_secret
                            }
                        }
                    }
                }
            }
        }
    }

    if config:
        if tenant in config['tenants']:
            if installation in config['tenants'][tenant]['installations']:
                config['tenants'][tenant]['installations'][installation]['environments'][environment] = new_config[
                    'tenants'][tenant]['installations'][installation]['environments'][environment]
            else:
                config['tenants'][tenant]['installations'][installation] = new_config['tenants'][tenant]['installations'][installation]
        else:
            config['tenants'][tenant] = new_config['tenants'][tenant]
    else:
        config = new_config

    with open(ctx.obj['CONFIG_PATH'], 'w') as file:
        click.echo(util.pretty_json(config), file=file)


@config.command()
@click.pass_context
def list(ctx):
    """
    Lists all configured credentials
    """
    if os.path.exists(ctx.obj['CONFIG_PATH']):
        with open(ctx.obj['CONFIG_PATH'], 'r') as file:
            config = json.loads(file.read())
            for tenant in config['tenants'].keys():
                for installation in config['tenants'][tenant]['installations'].keys():
                    for environment in config['tenants'][tenant]['installations'][installation]['environments'].keys():
                        click.echo(f"{tenant}:{installation}:{environment} Apikey ID: {config['tenants'][tenant]['installations'][installation]['environments'][environment]['apikey_id']}")
    else:
        click.echo(f"No configs found")
        exit(1)


@config.command()
@click.pass_context
@click.option('--tenant', required=True)
@click.option('--installation', required=True)
@click.option('--environment', required=True)
def remove(ctx, tenant, installation, environment):
    """
    Removes configured credentials
    """
    if os.path.exists(ctx.obj['CONFIG_PATH']):
        with open(ctx.obj['CONFIG_PATH'], 'r') as file:
            config = json.loads(file.read())
            if tenant in config['tenants']:
                if installation in config['tenants'][tenant]['installations']:
                    if environment in config['tenants'][tenant]['installations'][installation]['environments']:
                        config['tenants'][tenant]['installations'][installation]['environments'].pop(
                            environment)

                        if not config['tenants'][tenant]['installations'][installation]['environments'].keys():
                            config['tenants'][tenant]['installations'].pop(
                                installation)
                        if not config['tenants'][tenant]['installations'].keys():
                            config['tenants'].pop(tenant)

    else:
        click.echo(f"No configs found")
        exit(1)

    with open(ctx.obj['CONFIG_PATH'], 'w') as file:
        click.echo(util.pretty_json(config), file=file)
