import json
import os
import time

from aws_lambda_powertools.utilities.idempotency import DynamoDBPersistenceLayer, IdempotencyConfig, idempotent

EXPIRES_AFTER_SECONDS = 3 * 60  # 冪等性の期限[秒]

persistence_layer = DynamoDBPersistenceLayer(table_name=os.getenv("IDEMPOTENCY_STORE_TABLE_NAME"))

config = IdempotencyConfig(expires_after_seconds=EXPIRES_AFTER_SECONDS)
# config = IdempotencyConfig(event_key_jmespath="hoge_id", expires_after_seconds=EXPIRES_AFTER_SECONDS)


@idempotent(persistence_store=persistence_layer, config=config)
def handler(event, context):

    print(f"Lambdaが動いたー！！！{json.dumps(event)}")

    return {
        "hoge_id": event["hoge_id"],
        "message": "success",
        "statusCode": 200,
    }
