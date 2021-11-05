import os
import random

from aws_lambda_powertools.utilities.idempotency import IdempotencyConfig, idempotent
from custom_persistence_layer import CustomPersistenceLayer

EXPIRES_AFTER_SECONDS = 3 * 60  # 冪等性の期限[秒]

persistence_layer = CustomPersistenceLayer(table_name=os.getenv("IDEMPOTENCY_STORE_TABLE_NAME"))

config = IdempotencyConfig(expires_after_seconds=EXPIRES_AFTER_SECONDS)


@idempotent(persistence_store=persistence_layer, config=config)
def handler(event, context):

    return {
        "hoge_id": event["hoge_id"],
        "hoge_value": random.randint(0, 1000),
        "message": "success",
        "statusCode": 200,
    }
