import click
import json
from utils import util


@click.group()
def run_ids():
    """
    Functionality related to run id.
    """
    pass


@run_ids.command()
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--load-id')
@click.option('--source-entity-id')
@click.option('--target-entity-id')
@click.option('--source-run-id', type=int)
@click.option('--target-run-id', type=int)
@click.option('--days', type=int, help='How many days backwards is searched for')
@click.option('--limit', type=int, help='Max amount of results returned')
def search(ctx, environment_name, load_id, source_entity_id, target_entity_id, source_run_id, target_run_id, days, limit):
    """
    Search run ids stored in target environment
    """
    environment = util.get_environment_config_from_context(ctx, environment_name)
    s = util.create_session(environment)
    base_url = f"{ctx.obj['EXTERNAL_API_BASE_URL']}/external-api/api/{ctx.obj['TENANT']}/{ctx.obj['INSTALLATION']}/{environment_name.lower()}"

    params = []
    if load_id:
        params.append(f"loadId={load_id}")
    if source_entity_id:
        params.append(f"sourceEntityId={source_entity_id}")
    if target_entity_id:
        params.append(f"targetEntityId={target_entity_id}")
    if source_run_id:
        params.append(f"sourceRunId={source_run_id}")
    if target_run_id:
        params.append(f"targetRunId={target_run_id}")
    if days:
        params.append(f"days={days}")
    if limit:
        params.append(f"limit={limit}")

    response = search_run_ids(s, base_url, params)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))

@run_ids.command()
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--affected-rows')
@click.option('--target-entity-id', required=True)
@click.option('--target-run-id', type=int, required=True)
def add(ctx, environment_name, affected_rows, target_entity_id, target_run_id):
    """
    Add run ids to target env to be loaded.
    """
    environment = util.get_environment_config_from_context(ctx, environment_name)
    s = util.create_session(environment)
    base_url = f"{ctx.obj['EXTERNAL_API_BASE_URL']}/external-api/api/{ctx.obj['TENANT']}/{ctx.obj['INSTALLATION']}/{environment_name.lower()}"

    body = {}
    body['targetEntityId'] = target_entity_id
    body['targetRunId'] = target_run_id
    if affected_rows:
        body['affectedRows'] = affected_rows


    response = add_run_ids(s, base_url, json.dumps([body], cls=util.UUIDEncoder))
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))

@run_ids.command()
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--body', help='Request Body containing necessary infromation to add run ids')
def add_many(ctx, environment_name, body):
    """
    Add many run ids to target env to be loaded.

    Example value:

    \b
    [
        {
            "affectedRows": 4,
            "targetEntityId": "423389ff-8502-4b0a-8300-e12f57a00998",
            "targetRunId": 123
        }
    ]
    """
    if not body:
        stdin_stream = click.get_text_stream('stdin')
        if stdin_stream.isatty() is True:
            click.echo(
                f"Error: Missing either option '--body' and body could not be fetched from stdin.", err=True)
            exit(1)
        body = stdin_stream.read()

    environment = util.get_environment_config_from_context(ctx, environment_name)
    s = util.create_session(environment)
    base_url = f"{ctx.obj['EXTERNAL_API_BASE_URL']}/external-api/api/{ctx.obj['TENANT']}/{ctx.obj['INSTALLATION']}/{environment_name.lower()}"

    response = add_run_ids(s, base_url, body)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))

@run_ids.command()
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--load-id')
@click.option('--source-entity-id')
@click.option('--target-entity-id', required=True)
@click.option('--source-run-id', type=int)
@click.option('--target-run-id', type=int)
@click.option('--from-run-timestamp', type=int)
@click.option('--to-run-timestamp', type=int)
def delete(ctx, environment_name, load_id, source_entity_id, target_entity_id, source_run_id, target_run_id, from_run_timestamp, to_run_timestamp):
    """
    Deletes run ids according to given search criteria.
    """
    
    environment = util.get_environment_config_from_context(ctx, environment_name)
    s = util.create_session(environment)
    base_url = f"{ctx.obj['EXTERNAL_API_BASE_URL']}/external-api/api/{ctx.obj['TENANT']}/{ctx.obj['INSTALLATION']}/{environment_name.lower()}"

    params = []
    if load_id:
        params.append(f"loadId={load_id}")
    if source_entity_id:
        params.append(f"sourceEntityId={source_entity_id}")
    if target_entity_id:
        params.append(f"targetEntityId={target_entity_id}")
    if source_run_id:
        params.append(f"sourceRunId={source_run_id}")
    if target_run_id:
        params.append(f"targetRunId={target_run_id}")
    if from_run_timestamp:
        params.append(f"fromRunTimestamp={from_run_timestamp}")
    if to_run_timestamp:
        params.append(f"toRunTimestamp={to_run_timestamp}")

    delete_run_ids(s, base_url, params)
   

def search_run_ids(s, base_url, params):
    request_url = f"{base_url}/run-ids/v1/ids"
    if len(params) != 0:
        request_url = f"{request_url}?" + "&".join(params)

    response = s.get(request_url)
    content = json.loads(response.text) if response.text else ""

    if response.status_code == 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    elif response.status_code != 200:
        click.echo(
            f"Unable to search run ids with given parameters. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    return content


def add_run_ids(s, base_url, body):
    response = s.post(f"{base_url}/run-ids/v1/ids",
                      data=body)
    content = json.loads(response.text) if response.text else ""

    if response.status_code == 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    elif response.status_code != 200:
        click.echo(
            f"Unable to add run ids. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    return content

def delete_run_ids(s, base_url, params):
    request_url = f"{base_url}/run-ids/v1/ids"
    if len(params) != 0:
        request_url = f"{request_url}?" + "&".join(params)

    response = s.delete(request_url)
    content = json.loads(response.text) if response.text else ""

    if response.status_code == 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    elif response.status_code != 200:
        click.echo(
            f"Unable to delete run ids with given parameters. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
