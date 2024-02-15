import click
import json
from utils import util


@click.group()
def metadata_interface():
    """
    Functionality related to metadata interface.
    """
    pass



@metadata_interface.command()
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--query', required=True)
@click.option('--operation-name')
@click.option('--variables')
def graphql(ctx, environment_name, query, operation_name, variables):
    """
    Query metadata.
    """
    environment = util.get_environment_config_from_context(ctx, environment_name)
    s = util.create_session(environment)
    base_url = f"{ctx.obj['EXTERNAL_API_BASE_URL']}/external-api/api/{ctx.obj['TENANT']}/{ctx.obj['INSTALLATION']}/{environment_name.lower()}"

    body = {}
    body['query'] = query
    if operation_name:
        body['operationName'] = operation_name
    if variables:
        body['variables'] = variables

    print(json.dumps(body, cls=util.UUIDEncoder))
    response = query_graphql(s, base_url, json.dumps(body, cls=util.UUIDEncoder))
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))

@metadata_interface.command()
@click.pass_context
@click.option('--environment-name', required=True)
@click.option('--body', help='Request Body containing graphql query information.')
def graphql_json(ctx, environment_name, body):
    """
    Query metadata.

    Example value:

    \b
    {
        "query": "string",
        "operationName": "string",
        "variables": {
            "additionalProp1": {},
            "additionalProp2": {},
            "additionalProp3": {}
        }
    }
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

    response = query_graphql(s, base_url, body)
    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))

def query_graphql(s, base_url, body):
    response = s.post(f"{base_url}/metadata/v1/graphql",
                      data=body)
    content = json.loads(response.text) if response.text else ""

    if response.status_code == 401:
        click.echo(
            f"\nUnauthorized. Response code {response.status_code}", err=True)
        exit(1)
    if response.status_code == 400:
        click.echo(
            f"\nBad Request. Response code {response.status_code}", err=True)
        exit(1)
    elif response.status_code != 200:
        click.echo(
            f"Unable to query metadata. Response code {response.status_code}: \n{content}", err=True)
        exit(1)
    return content