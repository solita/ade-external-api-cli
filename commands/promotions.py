import json
import click
from utils import util


@click.group()
def promotions():
    """
    Functionality related to promotions.
    """
    pass


@promotions.command()
@click.pass_context
@click.option('--environment-name')
@click.option('--instance-id', type=click.UUID)
@click.option('--state', type=click.Choice(['DEMOTED', 'DEPLOYED', 'DEPLOYING', 'HISTORIZED', 'PROMOTED', 'WAITING']), multiple=True)
@click.option('--commit-id')
@click.option('--package-id', type=click.UUID)
@click.option('--created-from')
@click.option('--created-to')
@click.option('--updated-from')
@click.option('--updated-to')
@click.option('--size', type=int)
@click.option('--page', type=int)
def list(ctx, environment_name, instance_id, state, commit_id, package_id, created_from, created_to, updated_from, updated_to, size, page):
    """
    Gets all promotions with given filters
    """
    response = list_promotions(ctx, environment_name, instance_id, state, commit_id,
                               package_id, created_from, created_to, updated_from, updated_to, size, page)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


@promotions.command()
@click.pass_context
@click.option('--id', required=True, type=click.UUID)
def get(ctx, id):
    """
    Gets information about a promotion
    """
    response = get_promotion(ctx, id)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


@promotions.command()
@click.pass_context
@click.option('--commit-id', required=True, type=int)
@click.option('--description')
@click.option('--environment-name')
@click.option('--instance-id', type=click.UUID)
def promote(ctx, commit_id, description, environment_name, instance_id):
    """
    Promotes a commit to certain target instance
    """
    response = promote_commit(
        ctx, commit_id, description, environment_name, instance_id)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


@promotions.command()
@click.pass_context
@click.option('--id', required=True, type=click.UUID)
def demote(ctx, id):
    """
    Demotes a promotion
    """
    response = demote_promotion(ctx, id)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


@promotions.command()
@click.pass_context
@click.option('--source-instance-id', required=True, type=click.UUID)
@click.option('--target-instance-id', required=True, type=click.UUID)
@click.option('--all', is_flag=True, default=False, help='Enables promoting all deployed promotions from source environment')
def promote_env(ctx, source_instance_id, target_instance_id, all):
    """
    Promotes deployed promotions from one instance to another

    By default promotes only those packages which have been promoted 
    to the targeted instance. All packages can be forced to get promoted
    using --all flag

    """
    source_promotions = all_promotions_from_instance(
        ctx, source_instance_id, ['DEPLOYED'])
    target_promotions = all_promotions_from_instance(
        ctx, target_instance_id, ['DEPLOYED'])
    source_commit_ids = [(promotion["commitId"], promotion["packageId"])
                         for promotion in source_promotions]
    target_commit_ids = [(promotion["commitId"], promotion["packageId"])
                         for promotion in target_promotions]
    diff_commits = set(source_commit_ids) ^ (
        set(source_commit_ids) & set(target_commit_ids))
    if not all:
        filtered_commits = []
        for commit in diff_commits:
            if commit[1] in [tc[1] for tc in target_commit_ids]:
                filtered_commits.append(commit)
        diff_commits = filtered_commits

    with click.progressbar(diff_commits, label='Promoting commits') as bar:
        for commit in bar:
            promote_commit(
                ctx, commit[0], f"Promoted from instance with id: {source_instance_id}", None, target_instance_id)


@promotions.command()
@click.pass_context
@click.option('--instance-id', required=True, type=click.UUID)
def demote_promoted(ctx, instance_id):
    """
    Demotes all promoted promotions in a target instance
    """
    promotions = all_promotions_from_instance(ctx, instance_id, ['PROMOTED'])
    promotion_ids = [promotion["promotionId"] for promotion in promotions]

    with click.progressbar(promotion_ids, label='Demoting promotions') as bar:
        for promotion_id in bar:
            demote_promotion(ctx, promotion_id)


def list_promotions(ctx, environment_name, instance_id, state, commit_id, package_id, created_from, created_to, updated_from, updated_to, size, page):
    s = ctx.obj['SESSION']

    params = []
    if environment_name:
        params.append(f"environmentName={environment_name}")
    if instance_id:
        params.append(f"instanceId={instance_id}")
    if state:
        params.append(f"state=" + ",".join(state))
    if commit_id:
        params.append(f"commitId={commit_id}")
    if package_id:
        params.append(f"packageId={package_id}")
    if created_from:
        params.append(f"createdFrom={created_from}")
    if created_to:
        params.append(f"createdTo={created_to}")
    if updated_from:
        params.append(f"updatedFrom={updated_from}")
    if updated_to:
        params.append(f"updatedTo={updated_to}")
    if size:
        params.append(f"size={size}")
    if page:
        params.append(f"page={page}")

    request_url = f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/promotions"
    if len(params) != 0:
        request_url = f"{request_url}?" + "&".join(params)

    response = s.get(request_url)
    content = json.loads(response.text) if response.text else ""

    if response.status_code != 200:
        click.echo(
            f"Unable to list promotions with given parameters. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    elif response.status_code != 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    return content


def get_promotion(ctx, id):
    s = ctx.obj['SESSION']
    response = s.get(
        f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/promotions/{id}")
    content = json.loads(response.text) if response.text else ""

    if response.status_code != 200:
        click.echo(
            f"Unable to get promotion with id {id}. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    elif response.status_code != 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    return content


def promote_commit(ctx, commit_id, description, environment_name, instance_id):
    s = ctx.obj['SESSION']

    body = {}
    if commit_id:
        body['commitId'] = commit_id
    if description:
        body['description'] = description
    if environment_name:
        body['environmentName'] = environment_name
    if instance_id:
        body['environmentTargetInstanceId'] = instance_id

    response = s.post(f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/promotions",
                      data=json.dumps(body, cls=util.UUIDEncoder))
    content = json.loads(response.text) if response.text else ""

    if response.status_code != 200:
        click.echo(
            f"Unable to promote commit with id {commit_id}. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    elif response.status_code != 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    return content


def demote_promotion(ctx, id):
    s = ctx.obj['SESSION']
    response = s.delete(
        f"{ctx.obj['EXTERNAL_API_URL']}/deployment/v1/promotions/{id}")
    content = json.loads(response.text) if response.text else ""

    if response.status_code != 200:
        click.echo(
            f"Unable to demote promotion with id {id}. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    elif response.status_code != 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    return content


def all_promotions_from_instance(ctx, instance_id, states):
    pages = None
    current_page = 0
    source_promotions = []
    while pages is None or current_page < pages:
        response = list_promotions(
            ctx, None, instance_id, states, None, None, None, None, None, None, 1000, current_page)
        source_promotions.extend(response['content'])
        pages = response['totalPages']
        current_page = response['pageNumber'] + 1
    return source_promotions
