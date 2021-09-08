import click
import os
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
    if entity_id: request_url = request_url + f"?entityId={entity_id}"
    response = s.get(request_url)
    util.handleResponse(response.text, ctx.obj['FILE_WRITE'])
    return response


@code.command()
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--instance-id', required=True, type=click.UUID)
@click.option('--apikey', required=True)
@click.option('--apikey-secret', required=True)
def all_loads(ctx, environment_name, instance_id, apikey, apikey_secret):
    
    instance = json.loads(environments.get_instance(ctx, environment_name, instance_id).text)
    packages = [(promotion["packageId"], promotion["packageName"]) for promotion in promotions.all_promotions_from_instance(ctx,instance_id, ["DEPLOYED"])]

    s = ctx.obj['SESSION']
    s.headers.update({"X-API-KEY-ID": apikey, "X-API-KEY-SECRET": apikey_secret, "Content-Type": "application/json"})
    request_url = f"{ctx.obj['EXTERNAL_API_BASE_URL']}/external-api/api/{ctx.obj['TENANT']}/{ctx.obj['INSTALLATION']}/{environment_name}"

    if not os.path.exists("responses/results"):
        os.mkdir("responses/results")

    with click.progressbar(packages, label='Generating loads') as bar:
        for package in bar:
            response = s.get(f"{request_url}/code/v1/instances/{instance['instanceName']}/packages/{package[0]}/loads")
            f = open(f"responses/results/{package[1]}.json", "w")
            click.echo(util.prettyJson(response.text), file=f)
            f.close()
