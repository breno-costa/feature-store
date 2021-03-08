import click

from feature_store import main


@click.command()
def run():
    main.run()


if __name__ == '__main__':
    run()
