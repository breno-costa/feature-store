import click

from producer import producer


@click.command()
def run():
    producer.run(
        filepath="data/order.json.gz",
        filetype="json",
        key_field="order_id",
        timestamp_field="order_created_at",
        timestamp_format="%Y-%m-%dT%H:%M:%S.000Z",
        topic="orders"
    )


if __name__ == '__main__':
    run()
