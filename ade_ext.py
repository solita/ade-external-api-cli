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
def ade(ctx, tenant, installation, environment, apikey_id, apikey_secret, base_url, debug, file_write):
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

ade.add_command(code.code)
ade.add_command(commits.commits)
ade.add_command(deployments.deployments)
ade.add_command(environments.environments)
ade.add_command(promotions.promotions)

@ade.command()
def test():
    temp1 = [(1,"test1"), (2, "test2"), (6,"test4"), (7, "test5")]
    temp2 = [(2, "test2"), (4,"test4"), (5, "test5")]    
    # temp1_ids = [promotion["commitId"] for promotion in source_promotions]
    # temp2_commit_ids = [promotion["commitId"] for promotion in target_promotions]
    diff = set(temp1) ^ (set(temp1) & set(temp2))
    diff2 = []
    for f in diff:
        if f[1] in [t[1] for t in temp2]: 
            diff2.append(f[0])
    click.echo(diff2)