import click
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