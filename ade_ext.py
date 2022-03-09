import click
import http.client
import os
import json
from utils import util
from commands import config
from commands import commits
from commands import dagger
from commands import deployments
from commands import environments
from commands import packages
from commands import promotions
from commands import code
from commands import run_ids
from commands import load_status


@click.group()
@click.option('--tenant', envvar='ADE_TENANT', required=True, help="Tenant name used for calls")
@click.option('--installation', envvar='ADE_INSTALLATION', required=True, help="Installation name used for calls")
@click.option('--base-url', envvar='ADE_EXTERNAL_API_BASE_URL', default='https://external.services.saas.agiledataengine.com', help="Can be used to overwrite extenal api URL")
@click.option('--debug', is_flag=True, default=False, help="Enables debugging for http requests")
@click.option('--out', help="Output file name where response is written")
@click.option('--dir', help="Name of the folder where output is saved")
@click.pass_context
def ade(ctx, tenant, installation, base_url, debug, out, dir):
    """Agile Data Engine External API CLI tool.

    This tool is can be used to make requests to ADE External API. 
    It was created to provide to show example usage of the API and
    to help get started with more complex use scenarios.

    Usage requires setting up environment credentials using config
    command. Each call requires the user to specify which tenant and 
    installation should be used in the request. These can be specified 
    using options --tenant and --installation. Optionally you can specify
    them using environment variables:

    \b
    export ADE_TENANT=
    export ADE_INSTALLATION=

    """

    config_path = f"{click.get_app_dir(app_name='ade', roaming=False, force_posix=True)}/ade-ext-api-cli-config.json"
    ctx.ensure_object(dict)
    ctx.obj['CONFIG_PATH'] = config_path
    if click.get_current_context().invoked_subcommand != 'config':
        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                config = json.loads(file.read())
        else:
            click.echo(
                f"Configure credential using 'ade config' to before using the tool")
            exit(1)

        environment = {}
        if tenant in config['tenants'] and installation in config['tenants'][tenant]['installations']:
            for environment_name in config['tenants'][tenant]['installations'][installation]['environments'].keys():
                if config['tenants'][tenant]['installations'][installation]['environments'][environment_name]['type'] == 'design':
                    environment = config['tenants'][tenant]['installations'][installation]['environments'][environment_name]
                    break

        if not environment:
            click.echo(
                f"Configure design environment for tenant {tenant} and installation {installation}")
            exit(1)

        if debug:
            http.client.HTTPConnection.debuglevel = 1

        ctx.obj['SESSION'] = util.create_session(environment)
        ctx.obj['EXTERNAL_API_URL'] = f"{base_url}/external-api/api/{tenant}/{installation}/{environment_name}"
        ctx.obj['EXTERNAL_API_BASE_URL'] = base_url
        ctx.obj['TENANT'] = tenant
        ctx.obj['INSTALLATION'] = installation
        ctx.obj['CONFIG'] = config

        ctx.obj['OUT'] = out
        ctx.obj['DIR'] = dir


ade.add_command(config.config)
ade.add_command(code.code)
ade.add_command(commits.commits)
ade.add_command(dagger.dagger)
ade.add_command(deployments.deployments)
ade.add_command(environments.environments)
ade.add_command(packages.packages)
ade.add_command(promotions.promotions)
ade.add_command(run_ids.run_ids)
ade.add_command(load_status.load_status)
