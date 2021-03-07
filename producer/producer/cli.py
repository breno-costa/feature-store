import click

from producer import producer


@click.command()
@click.option("--filepath", help="Filepath to send to kafka")
@click.option("--topic")
@click.option("--filetype", default="json", help="Filetype (json, csv)")
@click.option("--key_field", default=None, help="")
@click.option("--timestamp_field", default=None)
@click.option("--timestamp_format", default="%Y-%m-%dT%H:%M:%S.000Z")
def run(filepath: str,
        topic: str,
        filetype: str = "json",
        key_field: str = None,
        timestamp_field: str = None,
        timestamp_format: str = "%Y-%m-%dT%H:%M:%S.000Z"):

    producer.run(
        filepath=filepath,
        filetype=filetype,
        key_field=key_field,
        timestamp_field=timestamp_field,
        timestamp_format=timestamp_format,
        topic=topic
    )


if __name__ == '__main__':
    run()
