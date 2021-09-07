import requests
import click
import http.client
from commands import commits 
from commands import deployments
from commands import environments 
from commands import promotions 
from commands import code


@click.group()
@click.option('--tenant', envvar='ADE_TENANT', required=True)
@click.option('--installation', envvar='ADE_INSTALLATION', required=True)
@click.option('--environment', envvar='ADE_ENVIRONMENT', required=True)
@click.option('--apikey-id', envvar='ADE_API_KEY_ID', required=True)
@click.option('--apikey-secret', envvar='ADE_API_KEY_SECRET', required=True)
@click.option('--base-url', envvar='ADE_EXTERNAL_API_BASE_URL', default='https://external.services.saasdev.agiledataengine.com')
@click.option('--debug', is_flag=True, default=False)
@click.option('--file-write')
@click.pass_context
def ext(ctx, tenant, installation, environment, apikey_id, apikey_secret, base_url, debug, file_write):
    if debug:
        http.client.HTTPConnection.debuglevel = 1
        click.echo(f"Tenant: {tenant}")
        click.echo(f"Installation: {installation}")
        click.echo(f"Environment: {environment}")
        click.echo(f"Api Key ID: {apikey_id}")
        click.echo(f"Api Key Secret: {apikey_secret}")


    s = requests.Session()
    s.headers.update({"X-API-KEY-ID": apikey_id, "X-API-KEY-SECRET": apikey_secret, "Content-Type": "application/json"})


    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug
    ctx.obj['SESSION'] = s
    ctx.obj['EXTERNAL_API_URL'] = base_url + "/external-api/api/" + tenant + "/" + installation + "/" + environment

    ctx.obj['FILE_WRITE'] = file_write

ext.add_command(code.code)
ext.add_command(commits.commits)
ext.add_command(deployments.deployments)
ext.add_command(environments.environments)
ext.add_command(promotions.promotions)
