import click
import json
from utils.versioned_group import VersionedGroup
from utils.versioned_command import VersionedCommand
from utils import util



@click.group(cls=VersionedGroup)
@click.option('--version', '-v', type=int, required=False, default=1, help='API version number')
def dagger(version):
    """
    Functionality related to dagger.
    """
    pass


@dagger.command(group='V1', cls=VersionedCommand)
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--dag-id', required=True, help='Dag name')
@click.option('--exec-date', required=True, help='The execDate is id of dag instance. This is returned when dag run is started by using POST method')
def get_v1(ctx, environment_name, dag_id, exec_date):
    """
    Query single dag run. 
    
    Notice that you need to know exact execDate (id of dag instance) to query info about it. 
    Basically you first create dagRun using POST method and then use returned execDate to query status.
    """

    environment = util.get_environment_config_from_context(
        ctx, environment_name)

    s = util.create_session(environment)
    base_url = f"{ctx.obj['EXTERNAL_API_BASE_URL']}/external-api/api/{ctx.obj['TENANT']}/{ctx.obj['INSTALLATION']}/{environment_name.lower()}"

    response = get_dag_run_v1(s, base_url, dag_id, exec_date)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))

@dagger.command(group='V1', cls=VersionedCommand)
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--dag-id', required=True, help='Dag name')
def start_v1(ctx, environment_name, dag_id):
    """
    Start dag run

    To start dag you need to know it's name. This method return info about created dag instance
    which can be used to query status afterwards by using GET method.
    """


    environment = util.get_environment_config_from_context(
        ctx, environment_name)

    s = util.create_session(environment)
    base_url = f"{ctx.obj['EXTERNAL_API_BASE_URL']}/external-api/api/{ctx.obj['TENANT']}/{ctx.obj['INSTALLATION']}/{environment_name.lower()}"

    response = start_dag_run_v1(s, base_url, dag_id)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


@dagger.command(group='V2', cls=VersionedCommand)
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--dag-id', required=True, help='Dag name')
@click.option('--dag-run-id', required=True, help='Dag run id')
def get_v2(ctx, environment_name, dag_id, dag_run_id):
    """
    Query single dag run.

    This can be used to query a single dag run. Notice that you need to know the dag run id to query info about it.
    Basically you first create dagRun using POST method and then use returned dagRunId to query status.
    """

    environment = util.get_environment_config_from_context(
        ctx, environment_name)

    s = util.create_session(environment)
    base_url = f"{ctx.obj['EXTERNAL_API_BASE_URL']}/external-api/api/{ctx.obj['TENANT']}/{ctx.obj['INSTALLATION']}/{environment_name.lower()}"

    response = get_dag_run_v2(s, base_url, dag_id, dag_run_id)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))

@dagger.command(group='V2', cls=VersionedCommand)
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--dag-id', required=True, help='Dag name')
@click.option('--state', type=click.Choice(['FAILED', 'NONE', 'NOT_SCHEDULED', 'QUEUED', 'RUNNING', 'SUCCESS']),
               multiple=True, help='Dag state to filter dag runs by certain state. ' +
               'To filter using multiple states, just set the state flag multiple times')
@click.option('--logical-date-from', help='Dag run logicalDate time filter range start value.')
@click.option('--logical-date-to', help='Dag run logicalDate time filter range end value.')
@click.option('--start-date-from', help='Dag run startDate time filter range start value.')
@click.option('--start-date-to', help='Dag run startDate time filter range end value.')
@click.option('--end-date-from', help='Dag run endDate time filter range end value.')
@click.option('--end-date-to', help='Dag run endDate time filter range end value.')
@click.option('--page', help='Page number used to offset the results. Only positive numbers allowed.')
@click.option('--size', help='The amount of results queried. Determines query page size. Allowed value range 0-100. Default page size is 100')
def find_v2(ctx, environment_name, dag_id, state, logical_date_from, logical_date_to, start_date_from, start_date_to, end_date_from, end_date_to, page, size):
    """
    Find dag runs.

    This can be used to find dag runs. You can use any combinations of parameters to filter dag runs.
    Notice that using '~' in place of dagId, you can query over all dags. Make sure to have '~' in parenthesis
    """

    environment = util.get_environment_config_from_context(
        ctx, environment_name)

    s = util.create_session(environment)
    base_url = f"{ctx.obj['EXTERNAL_API_BASE_URL']}/external-api/api/{ctx.obj['TENANT']}/{ctx.obj['INSTALLATION']}/{environment_name.lower()}"

    response = find_dag_runs_v2(s, base_url, dag_id, state, logical_date_from, logical_date_to,
                                start_date_from, start_date_to, end_date_from, end_date_to, page, size)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))

@dagger.command(group='V2', cls=VersionedCommand)
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--dag-id', required=True, help='Dag name')
def start_v2(ctx, environment_name, dag_id):
    """
    Start dag run

    To start dag you need to know it's name. This method return info about created dag instance
    which can be used to query status afterwards by using GET method.
    """
    environment = util.get_environment_config_from_context(
        ctx, environment_name)

    s = util.create_session(environment)
    base_url = f"{ctx.obj['EXTERNAL_API_BASE_URL']}/external-api/api/{ctx.obj['TENANT']}/{ctx.obj['INSTALLATION']}/{environment_name.lower()}"

    response = start_dag_run_v2(s, base_url, dag_id)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))



def get_dag_run_v1(s, base_url, dag_id, exec_date):
    response = s.get(f"{base_url}/dagger/v1/dags/{dag_id}/{exec_date}")
    content = json.loads(response.text) if response.text else ""

    if response.status_code == 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    elif response.status_code != 200:
        click.echo(
            f"Unable to get dag with given dag id {dag_id} and exec date {exec_date}. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    return content

def start_dag_run_v1(s, base_url, dag_id):
    response = s.post(f"{base_url}/dagger/v1/dags/{dag_id}")
    content = json.loads(response.text) if response.text else ""

    if response.status_code == 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    elif response.status_code != 201:
        click.echo(
            f"Unable to start dag with dag id {dag_id}. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    return content

def get_dag_run_v2(s, base_url, dag_id, dag_run_id):
    response = s.get(f"{base_url}/dagger/v2/dags/{dag_id}/dag-runs/{dag_run_id}")
    content = json.loads(response.text) if response.text else ""

    if response.status_code == 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    elif response.status_code != 200:
        click.echo(
            f"Unable to get dag with given dag id {dag_id} and exec date {dag_run_id}. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    return content


def start_dag_run_v2(s, base_url, dag_id):
    response = s.post(f"{base_url}/dagger/v2/dags/{dag_id}/dag-runs")
    content = json.loads(response.text) if response.text else ""

    if response.status_code == 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    elif response.status_code != 201:
        click.echo(
            f"Unable to start dag with dag id {dag_id}. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    return content

def find_dag_runs_v2(s, base_url, dag_id, state, logical_date_from, logical_date_to, start_date_from, start_date_to, end_date_from, end_date_to, page, size):

    params = []
    if state:
        params.append(f"state=" + ",".join(state))
    if logical_date_from:
        params.append(f"logicalDateFrom={logical_date_from}")
    if logical_date_to:
        params.append(f"logicalDateTo={logical_date_to}")
    if start_date_from:
        params.append(f"startDateFrom={start_date_from}")
    if start_date_to:
        params.append(f"startDateTo={start_date_to}")
    if end_date_from:
        params.append(f"endDateFrom={end_date_from}")
    if end_date_to:
        params.append(f"endDateTo={end_date_to}")
    if size:
        params.append(f"size={size}")
    if page:
        params.append(f"page={page}")

    request_url = f"{base_url}/dagger/v2/dags/{dag_id}/dag-runs"
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
            f"Unable to find dag runs with given parameters. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    return content