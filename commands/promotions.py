import json
import click
from utils import util

@click.group()
def promotions():
    pass


@promotions.command()
@click.pass_context
@click.option('--environment-name')
@click.option('--instance-id', type=click.UUID)
@click.option('--state', type=click.Choice(['DEMOTED', 'DEPLOYED', 'DEPLOYING', 'HISTORIZED', 'PROMOTED', 'WAITING']), multiple=True)
@click.option('--commit-id', type=click.UUID)
@click.option('--package-id', type=click.UUID)
@click.option('--created-from')
@click.option('--created-to')
@click.option('--updated-from')
@click.option('--updated-to')
@click.option('--size', type=int)
@click.option('--page', type=int)
def list(ctx, environment_name, instance_id, state, commit_id, package_id, created_from, created_to, updated_from, updated_to, size, page):

    s = ctx.obj['SESSION']

    request_url = ctx.obj['EXTERNAL_API_URL'] + "/deployment/v1/promotions"

    params = []
    if environment_name: params.append(f"environmentName={environment_name}")
    if instance_id: params.append(f"instanceId={instance_id}")
    if state: params.append(f"state=" + ",".join(state))
    if commit_id: params.append(f"commitId={commit_id}")
    if package_id: params.append(f"packageId={package_id}")
    if created_from: params.append(f"createdFrom={created_from}")
    if created_to: params.append(f"createdTo={created_to}")
    if updated_from: params.append(f"updatedFrom={updated_from}")
    if updated_to: params.append(f"updatedTo={updated_to}")
    if size: params.append(f"size={size}")
    if page: params.append(f"page={page}")

    if len(params) != 0: request_url = request_url + "?" + "&".join(params)

    response = s.get(request_url)
    util.handleResponse(response, ctx.obj['FILE_WRITE'])
    return response


@promotions.command()
@click.pass_context
@click.option('--promotion-id', required=True, type=click.UUID)
def get(ctx, promotion_id):
    s = ctx.obj['SESSION']
    request_url = ctx.obj['EXTERNAL_API_URL'] + "/deployment/v1/promotions/" + str(promotion_id)
    response = s.get(request_url)
    util.handleResponse(response, ctx.obj['FILE_WRITE'])
    return response


@promotions.command()
@click.pass_context
@click.option('--commit-id', type=int)
@click.option('--description')
@click.option('--environment-name')
@click.option('--instance-id', type=click.UUID)
def promote(ctx, commit_id, description, environment_name, instance_id):

    s = ctx.obj['SESSION']

    request_url = ctx.obj['EXTERNAL_API_URL'] + "/deployment/v1/promotions"

    body = {}
    if commit_id: body['commitId'] = commit_id
    if description: body['description'] = description
    if environment_name: body['environmentName'] = environment_name
    if instance_id: body['environmentTargetInstanceId'] = instance_id

    response = s.post(request_url, data=json.dumps(body, cls=util.UUIDEncoder))
    util.handleResponse(response, ctx.obj['FILE_WRITE'])
    return response


@promotions.command()
@click.pass_context
@click.option('--id', required=True, type=click.UUID)
def demote(ctx, id):
    s = ctx.obj['SESSION']
    request_url = ctx.obj['EXTERNAL_API_URL'] + "/deployment/v1/promotions/" + str(id)
    response = s.delete(request_url)
    util.handleResponse(response, ctx.obj['FILE_WRITE'])
    return response