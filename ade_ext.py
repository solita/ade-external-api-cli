import click
import http.client
import os
import json
from utils import util
from commands import commits 
from commands import deployments
from commands import environments 
from commands import promotions 
from commands import code


@click.group()
@click.option('--tenant', envvar='ADE_TENANT', required=True)
@click.option('--installation', envvar='ADE_INSTALLATION', required=True)
# @click.option('--environment', envvar='ADE_ENVIRONMENT', required=True)
# @click.option('--apikey-id', envvar='ADE_API_KEY_ID', required=True)
# @click.option('--apikey-secret', envvar='ADE_API_KEY_SECRET', required=True)
@click.option('--base-url', envvar='ADE_EXTERNAL_API_BASE_URL', default='https://external.services.saasdev.agiledataengine.com')
@click.option('--debug', is_flag=True, default=False)
@click.option('--out')
@click.option('--dir')
@click.pass_context
#, environment, apikey_id, apikey_secret
def ade(ctx, tenant, installation, base_url, debug, out, dir):
    if click.get_current_context().invoked_subcommand != 'config':
        if os.path.exists('.config'):
            with open ('.config', 'r') as file:
                config = json.loads(file.read())
        else:
            click.echo(f"Configure credential using 'ade config' to before using the tool")
            exit(1)

        environment = {}
        if tenant in config['tenants'] and installation in config['tenants'][tenant]['installations']:
            for environment_name in config['tenants'][tenant]['installations'][installation]['environments'].keys():
                if config['tenants'][tenant]['installations'][installation]['environments'][environment_name]['type'] == 'design':
                    environment = config['tenants'][tenant]['installations'][installation]['environments'][environment_name]
                    break

        if not environment:
            click.echo(f"Configure design environment for tenant {tenant} and installation {installation}")
            exit(1)

        if debug:
            http.client.HTTPConnection.debuglevel = 1

        s = util.create_session(environment)

        ctx.ensure_object(dict)
        ctx.obj['DEBUG'] = debug
        ctx.obj['SESSION'] = s
        ctx.obj['EXTERNAL_API_URL'] = f"{base_url}/external-api/api/{tenant}/{installation}/design"
        ctx.obj['EXTERNAL_API_BASE_URL'] = base_url
        ctx.obj['TENANT'] = tenant
        ctx.obj['INSTALLATION'] = installation
        ctx.obj['CONFIG'] = config

        ctx.obj['OUT'] = out
        ctx.obj['DIR'] = dir

@ade.command()
@click.option('--tenant', required=True)
@click.option('--installation', required=True)
@click.option('--environment', required=True)
@click.option('--apikey-id', required=True)
@click.option('--apikey-secret', required=True)
def config(tenant, installation, environment, apikey_id, apikey_secret):
    config = {}
    if os.path.exists('.config'):
        with open ('.config', 'r') as file:
            config = json.loads(file.read())


    new_config = {
        "tenants" : {
            tenant : {
                "installations": {
                    installation : {
                        "environments": {
                            environment : {
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
                    config['tenants'][tenant]['installations'][installation]['environments'][environment] = new_config['tenants'][tenant]['installations'][installation]['environments'][environment]
            else:
                config['tenants'][tenant]['installations'][installation] = new_config['tenants'][tenant]['installations'][installation]
    else:
        config = new_config

    with open ('.config', 'w') as file:
        click.echo(util.pretty_json(config), file=file)




ade.add_command(code.code)
ade.add_command(commits.commits)
ade.add_command(deployments.deployments)
ade.add_command(environments.environments)
ade.add_command(promotions.promotions)
