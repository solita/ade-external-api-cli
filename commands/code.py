import click
import json
from commands import environments
from commands import promotions
from utils import util


@click.group()
def code():
    """
    Functionality related to coded logic.
    """
    pass


@code.command()
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--instance-name', required=True)
@click.option('--package-id', required=True, type=click.UUID)
@click.option('--entity-id', type=click.UUID, help="Entity ID used to limit loads to certain entity")
def loads(ctx, environment_name, instance_name, package_id, entity_id):
    """
    Gets DvLoads for certain package
    """

    environment = util.get_environment_config_from_context(
        ctx, environment_name)

    s = util.create_session(environment)
    request_url = f"{ctx.obj['EXTERNAL_API_BASE_URL']}/external-api/api/{ctx.obj['TENANT']}/{ctx.obj['INSTALLATION']}/{environment_name.lower()}"

    response = get_loads(s, request_url, instance_name, package_id, entity_id)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


@code.command()
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--instance-id', required=True, type=click.UUID)
def all_loads(ctx, environment_name, instance_id):
    """
    Gets DvLoads for all packages in certain target instance
    """
    instance = environments.get_instance(ctx, environment_name, instance_id)
    packages = [(promotion["packageId"], promotion["packageName"])
                for promotion in promotions.all_promotions_from_instance(ctx, instance_id, ["DEPLOYED"])]

    environment = util.get_environment_config_from_context(
        ctx, environment_name)

    s = util.create_session(environment)
    request_url = f"{ctx.obj['EXTERNAL_API_BASE_URL']}/external-api/api/{ctx.obj['TENANT']}/{ctx.obj['INSTALLATION']}/{environment_name.lower()}"

    with click.progressbar(packages, label='Generating loads') as bar:
        for package in bar:
            response = get_loads(
                s, request_url, instance['instanceName'], package[0], None)
            if response:
                util.write_to_file(
                    ctx.obj['DIR'], f"{package[1]}.json", response)


def get_loads(s, base_url, instance_name, package_id, entity_id):
    url = f"{base_url}/code/v1/instances/{instance_name}/packages/{package_id}/loads"
    if entity_id:
        url = f"{url}?entityId={entity_id}"
    response = s.get(url)
    content = json.loads(response.text)
    if response.status_code == 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    elif response.status_code != 200:
        click.echo(
            f"\nLoad generation failed. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    return content
