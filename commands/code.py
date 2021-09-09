import click
import json
import requests
from commands import environments
from commands import promotions
from utils import util


@click.group()
def code():
    pass


@code.command()
@click.pass_context
@click.option('--instance-name', required=True)
@click.option('--package-id', required=True, type=click.UUID)
@click.option('--entity-id', type=click.UUID)
def loads(ctx, instance_name, package_id, entity_id):
    s = ctx.obj['SESSION']
    request_url = f"{ctx.obj['EXTERNAL_API_URL']}/code/v1/instances/{instance_name}/packages/{package_id}/loads"
    if entity_id:
        request_url = f"{request_url}?entityId={entity_id}"
    response = get_loads(s, request_url)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


@code.command()
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--instance-id', required=True, type=click.UUID)
@click.option('--apikey', required=True)
@click.option('--apikey-secret', required=True)
def all_loads(ctx, environment_name, instance_id, apikey, apikey_secret):
    
    instance = environments.get_instance(ctx, environment_name, instance_id)
    packages = [(promotion["packageId"], promotion["packageName"]) for promotion in promotions.all_promotions_from_instance(ctx, instance_id, ["DEPLOYED"])]

    s = requests.Session()
    s.headers.update({"X-API-KEY-ID": apikey, "X-API-KEY-SECRET": apikey_secret, "Content-Type": "application/json"})
    request_url = f"{ctx.obj['EXTERNAL_API_BASE_URL']}/external-api/api/{ctx.obj['TENANT']}/{ctx.obj['INSTALLATION']}/{environment_name.lower()}"

    with click.progressbar(packages, label='Generating loads') as bar:
        for package in bar:
            response = get_loads(s, request_url, instance['instanceName'], package[0], None)
            if response:
                util.write_to_file(ctx.obj['DIR'], f"{package[1]}.json", response)


def get_loads(s, url):
    response = s.get(url)
    content = json.loads(response.text)
    if response.status_code != 200:
                click.echo(f"\nLoad generation failed. Response code {response.status_code}: \n{content}", err=True)
                exit(1)
    return content