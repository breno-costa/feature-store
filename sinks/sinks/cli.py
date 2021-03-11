import click

from sinks import main


@click.command()
def run_sinks():
    main.start_sink_jobs()


if __name__ == '__main__':
    run_sinks()
