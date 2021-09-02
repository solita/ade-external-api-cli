import requests
import click
import http.client
from commands import commits 
from commands import deployments
from commands import environments 
from commands import promotions 


@click.group()
@click.option('--tenant', envvar='ADE_TENANT')
@click.option('--installation', envvar='ADE_INSTALLATION')
@click.option('--environment', envvar='ADE_ENVIRONMENT')
@click.option('--apikey-id', envvar='ADE_API_KEY_ID')
@click.option('--apikey-secret', envvar='ADE_API_KEY_SECRET')
@click.option('--base-url', envvar='ADE_EXTERNAL_API_BASE_URL', default='https://external.services.saasdev.agiledataengine.com')
@click.option('--debug', is_flag=True, default=False)
@click.option('--file-write', is_flag=True, default=False)
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

    if file_write: ctx.obj['FILE_WRITE'] = True
    else: ctx.obj['FILE_WRITE'] = False

ext.add_command(commits.commits)
ext.add_command(deployments.deployments)
ext.add_command(environments.environments)
ext.add_command(promotions.promotions)
