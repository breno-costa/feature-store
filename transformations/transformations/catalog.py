from transformations.definitions.customer_orders import CustomerOrdersOnLastDay
from transformations.definitions.order_creation import OrderCreation


# TODO: this list could be either fetched from the registry
#       or created at runtime
feature_groups = [
    CustomerOrdersOnLastDay(),
    OrderCreation()
]
