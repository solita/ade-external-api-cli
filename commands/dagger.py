import click
import json
from utils import util

@click.group()
def dagger():
    """
    Functionality related to dagger.
    """
    pass


@dagger.command()
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--dag-id', required=True, help='Dag name')
@click.option('--exec-date', required=True, help='The execDate is id of dag instance. This is returned when dag run is started by using POST method')
def get(ctx, environment_name, dag_id, exec_date):
    """
    Query single dag run. 
    
    Notice that you need to know exact execDate (id of dag instance) to query info about it. 
    Basically you first create dagRun using POST method and then use returned execDate to query status.
    """

    environment = util.get_environment_config_from_context(
        ctx, environment_name)

    s = util.create_session(environment)
    base_url = f"{ctx.obj['EXTERNAL_API_BASE_URL']}/external-api/api/{ctx.obj['TENANT']}/{ctx.obj['INSTALLATION']}/{environment_name.lower()}"

    response = get_dags(s, base_url, dag_id, exec_date)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))

@dagger.command()
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--dag-id', required=True, help='Dag name')
def start(ctx, environment_name, dag_id):
    """
    Start dag run

    To start dag you need to know it's name. This method return info about created dag instance
    which can be used to query status afterwards by using GET method.
    """

    environment = util.get_environment_config_from_context(
        ctx, environment_name)

    s = util.create_session(environment)
    base_url = f"{ctx.obj['EXTERNAL_API_BASE_URL']}/external-api/api/{ctx.obj['TENANT']}/{ctx.obj['INSTALLATION']}/{environment_name.lower()}"

    response = start_dag(s, base_url, dag_id)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


def get_dags(s, base_url, dag_id, exec_date):
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

def start_dag(s, base_url, dag_id):
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
