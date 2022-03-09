import click
import json
from utils import util


@click.group()
def load_status():
    """
    Functionality related to load status.
    """
    pass


@load_status.command()
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--load-id', required=True)
def get(ctx, environment_name, load_id):
    """
    Retrieves load status based on id.
    """
    
    environment = util.get_environment_config_from_context(ctx, environment_name)
    s = util.create_session(environment)
    base_url = f"{ctx.obj['EXTERNAL_API_BASE_URL']}/external-api/api/{ctx.obj['TENANT']}/{ctx.obj['INSTALLATION']}/{environment_name.lower()}"

    get_load_status(s, base_url, load_id)


@load_status.command()
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--load-id', required=True)
def delete(ctx, environment_name, load_id):
    """
    Deletes load status based on id.
    """
    
    environment = util.get_environment_config_from_context(ctx, environment_name)
    s = util.create_session(environment)
    base_url = f"{ctx.obj['EXTERNAL_API_BASE_URL']}/external-api/api/{ctx.obj['TENANT']}/{ctx.obj['INSTALLATION']}/{environment_name.lower()}"

    delete_load_status(s, base_url, load_id)


def get_load_status(s, base_url, load_id):
    request_url = f"{base_url}/loads/v1/{load_id}/status"

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

def delete_load_status(s, base_url, load_id):
    request_url = f"{base_url}/loads/v1/{load_id}/status"

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