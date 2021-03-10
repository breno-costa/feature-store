import click

from producer import file_producer


@click.command()
@click.option("--filepath", help="Filepath to send to kafka")
@click.option("--filetype", help="Filetype (json, csv)")
@click.option("--entity", help="Entity name")
@click.option("--entity_key", help="Field name used as entity id")
@click.option("--timestamp_field", help="Field name used as kafka timestamp")
@click.option("--timestamp_format", help="Format to convert timestamp fields (eg. %Y-%m-%dT%H:%M:%S.000Z)")
@click.option("--limit", type=int, help="Maximum number of records sent to kafka")
def run(filepath: str, filetype: str,
        entity: str, entity_key: str = None,
        timestamp_field: str = None,
        timestamp_format: str = "%Y-%m-%dT%H:%M:%S.000Z",
        limit: int = None):

    file_producer.run(
        filepath=filepath,
        filetype=filetype,
        entity=entity,
        entity_key=entity_key,
        timestamp_field=timestamp_field,
        timestamp_format=timestamp_format,
        limit=limit
    )


if __name__ == '__main__':
    run()
