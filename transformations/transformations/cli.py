import click

from transformations import main


@click.command()
def run_transformations():
    main.start_transformation_jobs()


if __name__ == '__main__':
    run_transformations()
