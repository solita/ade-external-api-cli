import json
import click
from utils import util

@click.group()
@click.pass_context
def promotions(ctx):
    ctx.obj['BASE_URL'] = f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/promotions"


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
    response = list_promotions(ctx, environment_name, instance_id, state, commit_id, package_id, created_from, created_to, updated_from, updated_to, size, page)
    if response.status_code == 200:
        util.handleResponse(response.text, ctx.obj['FILE_WRITE'])
        return response
    elif response.text != None:
        click.echo(f"{util.prettyJson(response.text)}", err=True)
    exit(1)
            

@promotions.command()
@click.pass_context
@click.option('--id', required=True, type=click.UUID)
def get(ctx, id):
    s = ctx.obj['SESSION']
    response = s.get(f"{ctx.obj['BASE_URL']}/{id}")
    util.handleResponse(response.text, ctx.obj['FILE_WRITE'])
    return response


@promotions.command()
@click.pass_context
@click.option('--commit-id', required=True, type=int)
@click.option('--description')
@click.option('--environment-name')
@click.option('--instance-id', type=click.UUID)
def promote(ctx, commit_id, description, environment_name, instance_id):
    response = promote_commit(ctx, commit_id, description, environment_name, instance_id)
    if response.status_code == 200 or response.status_code == 201:
        util.handleResponse(response.text, ctx.obj['FILE_WRITE'])
        return response
    elif response.text != None:
        click.echo(f"{util.prettyJson(response.text)}", err=True)
    exit(1)


@promotions.command()
@click.pass_context
@click.option('--id', required=True, type=click.UUID)
def demote(ctx, id):
    demote_promotion
    response = demote_promotion(ctx, id)
    if response.status_code == 200:
        util.handleResponse(response.text, ctx.obj['FILE_WRITE'])
        return response
    elif response.text != None:
        click.echo(f"{util.prettyJson(response.text)}", err=True)
    exit(1)


@promotions.command()
@click.pass_context
@click.option('--source-instance-id', required=True, type=click.UUID)
@click.option('--target-instance-id', type=click.UUID)
def promote_env(ctx, source_instance_id, target_instance_id):
    source_promotions = all_promotions_from_instance(ctx, source_instance_id, ['DEPLOYED'])
    target_promotions = all_promotions_from_instance(ctx, target_instance_id, ['DEPLOYED'])
    source_commit_ids = [promotion["commitId"] for promotion in source_promotions]
    target_commit_ids = [promotion["commitId"] for promotion in target_promotions]
    diff_commits = set(source_commit_ids) ^ (set(source_commit_ids) & set(target_commit_ids))

    for commit_id in diff_commits:
        promote_commit(ctx, commit_id, f"Promoted from instance with id: {source_instance_id}", None, target_instance_id)


@promotions.command()
@click.pass_context
@click.option('--instance-id', required=True, type=click.UUID)
def demote_promoted(ctx, instance_id):
    promotions = all_promotions_from_instance(ctx, instance_id, ['PROMOTED'])
    promotion_ids = [promotion["promotionId"] for promotion in promotions]

    for promotion_id in promotion_ids:
        demote_promotion(ctx, promotion_id)



def list_promotions(ctx, environment_name, instance_id, state, commit_id, package_id, created_from, created_to, updated_from, updated_to, size, page):
    s = ctx.obj['SESSION']

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

    request_url = ctx.obj['BASE_URL']
    if len(params) != 0: request_url = f"{request_url}?" + "&".join(params)

    return s.get(request_url)

def all_promotions_from_instance(ctx, instance_id, states):
    pages = None
    current_page = 0
    source_promotions = []
    while pages == None or current_page < pages:
        click.echo(f"pages: {pages}")
        click.echo(f"current_page: {current_page}")
        source_response = list_promotions(ctx, None, instance_id, states, None, None, None, None, None, None, 1000, current_page)
        if source_response.status_code == 200:
            promotions = json.loads(source_response.text)
            source_promotions.extend(promotions['content'])
            pages = promotions['totalPages']
            current_page = promotions['pageNumber'] + 1
        else:
            exit(1)
    return source_promotions


def demote_promotion(ctx, id):
    s = ctx.obj['SESSION']
    response = s.delete(f"{ctx.obj['BASE_URL']}/{id}")
    return response


def promote_commit(ctx, commit_id, description, environment_name, instance_id):
    s = ctx.obj['SESSION']

    body = {}
    if commit_id: body['commitId'] = commit_id
    if description: body['description'] = description
    if environment_name: body['environmentName'] = environment_name
    if instance_id: body['environmentTargetInstanceId'] = instance_id

    response = s.post(ctx.obj['BASE_URL'], data=json.dumps(body, cls=util.UUIDEncoder))
    return response